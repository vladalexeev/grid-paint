// RaphaelJS documentation - http://raphaeljs.com/reference.html
// JQuery Minicolors color picker documentation - http://labs.abeautifulsite.net/jquery-miniColors/
// Tag manager - http://welldonethings.com/tags/manager


var mode="paint"; //available values "paint", "pick-color", "copy", "paste"
var paper;
var grid;
var selectedShapeName=null;
var selectedColor="#3377ee";
var backgroundColor="#ffffff";
var recentColors=[];
var changed=false;
var paperMouseDown=false;

var shapesToolbarGrid;

var gridArtwork=new GridArtwork();
var workspaceWidth;
var workspaceHeight;

var undoStack=[];
var redoStack=[];

var selection=new GridSelection();

var drawToolProperties = {};
var drawToolTemporaryCells = [];
var drawToolTemporaryShapes = {};

var modalDescriptionVisible = false;
var modalTagsVisible = false;
var modalSquareGridSpecialPropertiesVisible = false;
var initialTagsValue = null;

var socket = null;
var collaboratorsOnline = [];
var collaboratorBadges = [];

// 
function adjustCanvasWrapper() {
	$("#canvas-wrapper").height($(window).height()-60);
	$(".painter-toolbar-full").height($(window).height()-60);
}

function paintShapeToolButton(shapeName) {
	var shape=shapesToolbarGrid.shapes[shapeName];
	
	$("#shape-"+shapeName).html("");

	var shapeRect=shapesToolbarGrid.getCellRect(0,0);
	var shapePaper=new Raphael("shape-"+shapeName, shapeRect.width+20, shapeRect.height+20);
	
	if (shapeName==selectedShapeName) {
		var bgElement=shapePaper.ellipse(shapeRect.width/2+10, shapeRect.height/2+10,
			shapeRect.width/2+10, shapeRect.height/2+10);
		bgElement.attr({"fill":"r#ffffff:40-#cccccc", "stroke-width":0});
	}
	shape.paint(shapePaper, 0, 0, selectedColor, 10, 10);
}

function selectShape(shapeName) {
	var oldSelectedShapeName=selectedShapeName;
	selectedShapeName=shapeName;
	for (var shapeName in grid.shapes) {
		if (shapeName==selectedShapeName ||
			shapeName==oldSelectedShapeName) {
			paintShapeToolButton(shapeName);		
		}
	}
}

function paintOnCanvas(col, row, shapeName, color) {
	var cell=gridArtwork.setCell(col, row, shapeName, color);
	if (!cell.element && cell.shapeName!="empty") {
		var element=grid.shapes[shapeName].paint(paper, col, row, color, 0, 0);
		cell.element=element;
	}
}

/**
 * Return cell coordintes {row: XXX, col: XXX} by mouse event 
 */
function getCellCoordByMouseEvent(event) {
  	return grid.pointToCell(
			event.pageX - $("#canvas").position().left,
			event.pageY - $("#canvas").position().top);
}

function updateCellCoordiantesPanel(event) {
	var cell=getCellCoordByMouseEvent(event);
	$("#coordinates").text(cell.col+" "+cell.row);
}

function storeUndoCell(col, row, newShapeName, newColor) {
	var oldCell=gridArtwork.getCell(col, row);
	var oldShapeName="empty";
	var oldColor="#ffffff";
	if (oldCell) {
		oldShapeName=oldCell.shapeName;
		oldColor=oldCell.color;
	}
	
	undoStack[undoStack.length-1].pushCellChange(
		col, row, 
		oldShapeName, newShapeName,
		oldColor, newColor);
}

function paintOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
			
	if (paperMouseDown) {
		newShapeName=selectedShapeName;
		if (event.which==3) {
			newShapeName="empty";
		}

		// Return immediately if there are no actual changes
		var oldCell = gridArtwork.getCell(cell.col, cell.row);
		if ((oldCell == null || oldCell.shapeName == 'empty') && newShapeName == 'empty') {
			return;
		}
		if (oldCell != null && oldCell.shapeName == newShapeName && oldCell.color == selectedColor) {
			return;
		}
		
		storeUndoCell(cell.col, cell.row, newShapeName, selectedColor);
		paintOnCanvas(cell.col, cell.row, newShapeName, selectedColor);
		if (newShapeName!="empty") {
			pushRecentColor(selectedColor);	
		}
		changed=true;

		if (socket != null) {
			var changes = {
				'cells': [{
					col: cell.col,
					row: cell.row,
					shapeName: newShapeName,
					color: selectedColor
				}]
			}
			console.log('socket.io <- changes (paintOnCanvasByMouseEvent)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}
}

function eraseOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
	if (paperMouseDown) {
		// Return immediately if there are no actual changes
		var oldCell = gridArtwork.getCell(cell.col, cell.row);
		if (oldCell == null || oldCell.shapeName == 'empty') {
			return;
		}

		storeUndoCell(cell.col, cell.row, 'empty', selectedColor);	
		paintOnCanvas(cell.col, cell.row, 'empty', selectedColor);
		changed=true;

		if (socket != null) {
			var changes = {
				'cells': [{
					col: cell.col,
					row: cell.row,
					shapeName: 'empty',
					color: selectedColor
				}]
			}
			console.log('socket.io <- changes (eraseOnCanvasByMouseEvent)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}
}

function selectOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
	
	if (paperMouseDown) {
		var oldCell=gridArtwork.getCell(cell.col, cell.row);
		
		var cellShapeName="empty";
		var cellColor="#ffffff";
		if (oldCell) {
			cellShapeName=oldCell.shapeName;
			cellColor=oldCell.color;
		}
		
		if (event.which==3) {
			selection.forgetCell(cell.col, cell.row);
		} else {
			selection.saveCell(cell.col, cell.row, cellShapeName, cellColor);
		}
	}
}

function changePastePositionByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
	var nearestCell=grid.nearestSameCell(selection.baseCol, selection.baseRow, cell.col, cell.row);
	selection.changePasteCell(nearestCell.col, nearestCell.row);
	
}

function pickColorByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
	var cellItem=gridArtwork.getCell(cell.col, cell.row);
	if (cellItem) {
		selectColor(cellItem.color);
		$("#btn-pick-color").button("toggle");
		setMode("paint");
		
		if (selectedShapeName=="empty") {
			selectShape("flat");
		}
	}
}

function draftDrawToolOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);

	var toolName = mode;

	if (paperMouseDown) {
	    if (!drawToolProperties['startCell']) {
			drawToolProperties['startCell'] = cell;
			drawToolProperties['endCell'] = cell;
	    } else {
			var startCell = drawToolProperties['startCell'];
			var endCell = drawToolProperties['endCell'];
			if (event.ctrlKey) {
				cell = grid.drawTools[toolName].adjustEndCell(startCell, cell);
			}

			if (startCell.col == cell.col && startCell.row == cell.row) {
				// Line with zero length
				for (var i = 0; i < drawToolTemporaryCells.length; i++) {
					var key = cellKey(drawToolTemporaryCells[i]);
					drawToolTemporaryShapes[key].remove();
					delete drawToolTemporaryShapes[key];
				}
				drawToolTemporaryCells = [];
				drawToolTemporaryShapes = {};
				endCell = cell;
				return;
			}

			if (endCell.col == cell.col && endCell.row == cell.row) {
				return;
			}
			drawToolProperties['endCell'] = cell;
			endCell = cell;
			var newTemporaryCells = grid.drawTools[toolName].calculateCells(startCell, endCell);

			for (var i = 0; i < drawToolTemporaryCells.length; i++) {
				var found = false;
				var oldKey = cellKey(drawToolTemporaryCells[i]);
				for (var j=0; j < newTemporaryCells.length; j++) {
					var newKey = cellKey(newTemporaryCells[j])
					if (oldKey == newKey) {
						found = true;
						break;
					}
				}
				if (!found && drawToolTemporaryShapes[oldKey]) {
					drawToolTemporaryShapes[oldKey].remove();
					delete drawToolTemporaryShapes[oldKey];
				}
			}

			for (var i = 0; i < newTemporaryCells.length; i++) {
				var newKey = cellKey(newTemporaryCells[i]);
				var found = false;
				for (var j = 0; j < drawToolTemporaryCells.length; j++) {
					var oldKey = cellKey(drawToolTemporaryCells[j]);
					if (newKey == oldKey) {
						found = true;
						break;
					}
				}
				if (!found) {
					var cell = newTemporaryCells[i]
					var element = grid.internalShapes["selected"].paint(paper, cell.col, cell.row, "#ffffff", 0, 0);	
					drawToolTemporaryShapes[newKey] = element;
				}
			}

			drawToolTemporaryCells = newTemporaryCells;
	    }
	}
}

function drawToolOnCanvas() {
    if (drawToolProperties['startCell'] && drawToolProperties['endCell']) {
        var startCell = drawToolProperties['startCell'];
        var endCell = drawToolProperties['endCell'];
        var cells = drawToolTemporaryCells;
        for (var i=0; i < cells.length; i++) {
            storeUndoCell(cells[i].col, cells[i].row, selectedShapeName, selectedColor);
            paintOnCanvas(cells[i].col, cells[i].row, selectedShapeName, selectedColor);
		}
		
		for (var i = 0; i < cells.length; i++) {
			var key = cellKey(cells[i]);
			drawToolTemporaryShapes[key].remove();
		}
        drawToolProperties = {};
		drawToolTemporaryCells = [];
		drawToolTemporaryShapes = {};

		if (selectedShapeName!="empty") {
			pushRecentColor(selectedColor);	
		}
	
		changed = true;
		
		if (socket != null) {
			var changes = {
				cells: []
			}
			for (var i=0; i < cells.length; i++) {
				changes.cells.push({
					col: cells[i].col,
					row: cells[i].row,
					shapeName: selectedShapeName,
					color: selectedColor
				})
			}
	
			console.log('socket.io <- changes (drawToolOnCanvas)');
			console.log(changes);
			socket.emit('changes', changes);
		}
    }
}


function getArtworkEffectiveRect(grid, artwork) {
	var x1=100000;
	var y1=100000;
	var x2=0;
	var y2=0;
	for (var row=0; row<artwork.cells.length; row++) {
		for (var col=0; col<artwork.cells[row].length; col++) {
			if (artwork.cells[row][col] && artwork.cells[row][col].shapeName!='empty') {
				var cellRect=grid.getCellRect(col, row);
				if (cellRect.left<x1) {
					x1=cellRect.left;
				}
				if (cellRect.top<y1) {
					y1=cellRect.top;
				}
				if (cellRect.left+cellRect.width>x2) {
					x2=cellRect.left+cellRect.width;
				}
				if (cellRect.top+cellRect.height>y2) {
					y2=cellRect.top+cellRect.height;
				}
			}
		}
	}
	
	return {
		left: Math.floor(x1),
		top: Math.floor(y1),
		width: Math.round(x2-x1+1),
		height: Math.round(y2-y1+1)
	};
}

function getArtworkEffectivePixelArtRect(grid, artwork) {
	var x1=100000;
	var y1=100000;
	var x2=0;
	var y2=0;
	for (var row=0; row<artwork.cells.length; row++) {
		for (var col=0; col<artwork.cells[row].length; col++) {
			if (artwork.cells[row][col] && artwork.cells[row][col].shapeName!='empty') {
				if (row<y1) {
					y1=row;
				}
				
				if (row>y2) {
					y2=row;
				}
				
				if (col<x1) {
					x1=col;
				}
				
				if (col>x2) {
					x2=col;
				}
			}
		}
	}
	
	return {
		left: x1,
		top: y1,
		width: x2-x1+1,
		height: y2-y1+1
	};
}

function riseUpButton(selector) {
	if ($(selector).attr('aria-pressed')=='true') {
		$(selector).button('toggle');
	}
}

function setMode(m) {
	if (mode=='copy') {
		selection.copyFinished();
	}
	
	if (mode=='paste') {
		selection.pasteFinished();
	}
	
	$('#btn-pencil').removeClass('active').removeAttr("disabled");
	$('#btn-pick-color').removeClass('active').removeAttr("disabled");
	$('#btn-flood-fill').removeClass('active').removeAttr("disabled");
	$('#btn-draw-line').removeClass('active').removeAttr("disabled");
	$("#btn-copy-mode").removeClass('active').removeAttr("disabled");
	$("#btn-paste-mode").removeClass('active').removeAttr("disabled");
	$("#btn-erase").removeClass('active').removeAttr("disabled");

	if (grid.drawTools) {
		for (var toolName in grid.drawTools) {
			$('.btn-draw-tool[tool-name='+toolName+']').removeClass('active').removeAttr("disabled");
		}
	}
	
	
	mode=m;
	if (mode=="paint") {
		$("#canvas-wrapper").css("cursor","crosshair");
		$('#btn-pencil').addClass('active');
	} else if (mode=="pick-color") {
		$("#canvas-wrapper").css("cursor","url(/img/cursors/pick-color.png) 2 32, crosshair");
		$('#btn-pick-color').addClass('active');
	} else if (mode=="copy") {
		$("#canvas-wrapper").css("cursor","url(/img/cursors/mark-area.png) 8 8, crosshair");
		$('#btn-copy-mode').addClass('active');	
		selection.copyPrepare();	
	} else if (mode=="paste") {
		$("#canvas-wrapper").css("cursor","crosshair"); // TODO change cursor
		$('#btn-paste-mode').addClass('active');
		selection.pastePrepare();
	} else if (mode=='fill') {
		$("#canvas-wrapper").css("cursor","url(/img/cursors/flood-fill.png) 2 32, crosshair");
		$('#btn-flood-fill').addClass('active');
	} else if (mode=='erase') {
		$("#canvas-wrapper").css("cursor","url(/img/cursors/eraser.png) 8 32, crosshair");
		$('#btn-erase').addClass('active');
	} else if (grid.drawTools[mode]) {
		$("#canvas-wrapper").css("cursor","crosshair");
		$('.btn-draw-tool[tool-name='+mode+']').addClass('active');
	}
}

function prepareArtworkToSave() {
	var a={
		version: {
			major:2,
			minor:0
		},
		effectiveRect: getArtworkEffectiveRect(grid,gridArtwork),
		canvasSize: {
			width: grid.workspaceWidth,
			height: grid.workspaceHeight
		},
		backgroundColor: backgroundColor,
		layers:[{
			grid:grid.name,
			cellSize:grid.cellSize,
			gridThickness: grid.gridThickness,
			gridColor: grid.gridColor,
			rows:[]
		}],
		recentColors: recentColors
	};

	if (grid.name=='square') {
		a['effectivePixelArtRect'] = getArtworkEffectivePixelArtRect(grid, gridArtwork);
	}

	a['transparentBackground'] = $('#modal_transparent_background')[0].checked;
	a['gridVisible'] = $('#modal_artwork_grid_visible')[0].checked;
	a['additionalPixelImage'] = $('#modal_artwork_pixel_art')[0].checked;

	if (artwork.id) {
		a.id=artwork.id;
	}

	for (var row=0; row<gridArtwork.cells.length; row++) {
		var rowElement={
			row:row
		};
		var cellArray=[];

		for (var col=0; col<gridArtwork.cells[row].length; col++) {
			if (gridArtwork.cells[row][col] && gridArtwork.cells[row][col].shapeName!="empty") {
				cellArray.push([
					col,
					gridArtwork.cells[row][col].shapeName,
					gridArtwork.cells[row][col].color
				]);
			}
		}

		if (cellArray.length > 0) {
			rowElement.cells=cellArray;
			a.layers[0].rows.push(rowElement);
		}
	}

    return a;
}

function saveArtwork() {
    var a = prepareArtworkToSave();

	if (a.effectiveRect.width<0 || a.effectiveRect.height<0) {
		var messageModal=$("#message-modal");
		messageModal.find("#message-text").text("Cannot save empty image");
		messageModal.modal();
		return;
	}

    $("input[name=artwork_json]").val(JSON.stringify(a));
    changed=false;
    showCircleLoader();
    $.ajax({
		type: 'post',
		url: '/json/save-image',
		data: $("form[name=f]").serialize(),
		dataType: "json",
		success: function(data) {
		    if (data.error) {
		        hideCircleLoader();
		        if (data.error === 'few_pixels') {
		            showWarningMessage('The image contains too few pixels. Please, create more complex image.');
		        } else {
		            showWarningMessage("Something went wrong. Try again.");
		        }
		        return;
		    }
		    if (data.result) {
    		    var artwork_id = data.result;
    		    var artwork_tags = $('input[name=artwork_tags]').val()
    		    if (initialTagsValue == artwork_tags) {
    		        document.location = '/images/details/' + artwork_id;
    		    } else {
                    $.ajax({
                        type: 'post',
                        url: '/json/save-image-tags',
                        data: {
                            artwork_id: artwork_id,
                            artwork_tags: artwork_tags
                        },
                        dataType: 'json',
                        success: function(data) {
                            document.location = '/images/details/' + artwork_id
                        },
                        error: function() {
                            hideCircleLoader();
                            showWarningMessage("Something went wrong. Try again.")
                        }
                    })
    		    }
			} else {
				hideCircleLoader();
			}
		},
		error: function() {
			hideCircleLoader();
			showWarningMessage("Something went wrong. Try again.")
		}
	});
}

function propertiesDialog_updateDescriptionLabelPreview() {
	var description = $('#modal_artwork_description').val();
	$('#modal_description_label').find('.save-dialog-expandable-content-preview').text(description);
}

function propertiesDialog_updateTagsLabelPreview() {
	var tags = $('#modal_artwork_tags').val();
	var text = '';
	if (tags) {
	    var tagsList = tags.split(',');
	    for (var i = 0; i < tagsList.length; i++) {
	        if (i > 0) {
	            text += ' ';
	        }
	        text += '#' + tagsList[i];
	    }
	}
	$('#modal_tags_label').find('.save-dialog-expandable-content-preview').text(text);
}

function showPropertiesDialog(modalAction) {
	if (artwork.layers[0].grid=='square') {
		$("#modal_square_grid_special_properties").show();
	} else {
		$("#modal_square_grid_special_properties").hide();
	}

    propertiesDialog_updateDescriptionLabelPreview();
    propertiesDialog_updateTagsLabelPreview();

	$("#modal_success_action").val(modalAction);
	$("#properties-modal").modal('show');
}

/*
 * Push color of the last painted shape to palette
 */
function pushRecentColor(hexColor) {
	pushColor=hexColor;
	for (var i=0; i<recentColors.length; i++) {
		var oldColor=recentColors[i];
		recentColors[i]=pushColor;
		pushColor=oldColor;
		if (oldColor==hexColor) {
			break;
		}
	}
	
	$paletteDivs=$("#color-palette div");
	for (var i=0; i<$paletteDivs.length && i<recentColors.length; i++) {
		$($paletteDivs[i]).css("background-color",recentColors[i]);
	}	
}

function selectColorFromPicker(hexColor) {
	if (selectedColor.toUpperCase()==hexColor.toUpperCase()) {
		return;
	}
	
	selectedColor=hexColor;
	for (var shapeName in grid.shapes) {
		paintShapeToolButton(shapeName);
		$("#selected-color").css("background-color",selectedColor);
	}
	
	var colorInText = $("#color-picker-text").val();
	if (colorInText.toUpperCase != hexColor.toUpperCase()) { 
		$("#color-picker-text").val(hexColor);
	}	
}

function calculateFillArea(cell) {
	var gridCell=gridArtwork.getCell(cell.col, cell.row);
	var sourceColorShape='empty';
	if (gridCell) {
		if (gridCell.shapeName !== 'empty') {
			sourceColorShape = gridCell.shapeName + '-' + gridCell.color;
		}
	}
	
	var colCount=workspaceWidth/grid.cellSize;
	var rowCount=workspaceHeight/grid.cellSize;
	
	var currentCells=[{
		row: cell.row,
		col: cell.col	
	}];
	var result=[{
		row: cell.row,
		col: cell.col			
	}];
	
	var testFill=function(col, row) {
		var testCell=gridArtwork.getCell(col, row);
		var testColorShape='empty';
		if (testCell) {
			if (testCell.shapeName !== 'empty') {
				testColorShape = testCell.shapeName + '-' + testCell.color;
			}
		}	
		if (testColorShape!=sourceColorShape) {
			return false;
		}
		for (var i=0; i<result.length; i++) {
			if (result[i].col==col && result[i].row==row) {
				return false;
			}
		}
		return true;
	};
	
	while (currentCells.length>0) {
		var newCells=[];
		for (var i=0; i<currentCells.length; i++) {
			var currentCell=currentCells[i];
			var adjacentCells=grid.getAdjacentCells(currentCell.col, currentCell.row)
			for (var j=0; j<adjacentCells.length; j++) {
				var testCell=adjacentCells[j]
				if (!grid.isCellInsideWorkspace(testCell.col, testCell.row)) {
					return [];
				}
				
				if (testFill(testCell.col, testCell.row)) {
					newCells.push(testCell);
					result.push(testCell);
				}
			}
		}
		currentCells=newCells;
	}
	
	return result;
}

function fillAreaOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
			
	if (paperMouseDown) {
		paperMouseDown=false;
		newShapeName=selectedShapeName;
		if (event.which==3) {
			newShapeName="empty";
		}
		
		var fillCells=calculateFillArea(cell);
		if (fillCells.length==0) {
			showWarningMessage('You cannot fill entire workspace with flood fill tool. It is applicable for closed areas only. Use "Set background color" instead.');
			return;
		} 
		
		for (var i=0; i<fillCells.length; i++) {
			var currentCell=fillCells[i];
			storeUndoCell(currentCell.col, currentCell.row, newShapeName, selectedColor);
			paintOnCanvas(currentCell.col, currentCell.row, newShapeName, selectedColor);
		}
		
		if (newShapeName!="empty") {
			pushRecentColor(selectedColor);	
		}
		
		changed=true;

		if (socket != null) {
			var changes = {
				cells: []
			}
			for (var i=0; i < fillCells.length; i++) {
				changes.cells.push({
					col: fillCells[i].col,
					row: fillCells[i].row,
					shapeName: newShapeName,
					color: selectedColor
				})
			}
	
			console.log('socket.io <- changes (fillAreaOnCanvasByMouseEvent)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}
}

function selectColorFromText(hexColor) {
	if (selectedColor.toUpperCase()==hexColor.toUpperCase()) {
		return;
	}
	
	var testColor = /^#[0-9A-Fa-f]{6}$/i.test(hexColor);
	
	if (hexColor.length!=7 || !testColor) {
		return;
	}
	
	if (hexColor.toUpperCase()==selectedColor.toUpperCase()) {
		return;
	}
	
	selectedColor=hexColor;
	
	for (var shapeName in grid.shapes) {
		paintShapeToolButton(shapeName);
		$("#selected-color").css("background-color",selectedColor);
	}
	
	$("#color-picker").minicolors("value",hexColor);
}

function selectColor(hexColor) {
	if (selectedColor.toUpperCase()==hexColor.toUpperCase()) {
		return;
	}
	
	selectedColor=hexColor;
	for (var shapeName in grid.shapes) {
		paintShapeToolButton(shapeName);
		$("#selected-color").css("background-color",selectedColor);
	}
	
	var colorInText = $("#color-picker-text").val();
	if (colorInText.toUpperCase != hexColor.toUpperCase()) { 
		$("#color-picker-text").val(hexColor);
	}
	
	$("#color-picker").minicolors("value",hexColor);
}

function updateUndoRedoButtons() {
	if (undoStack.length>0) {
		$("#btn-undo").removeAttr("disabled");
	} else {
		$("#btn-undo").attr("disabled", "disabled");
	}
	
	if (redoStack.length>0) {
		$("#btn-redo").removeAttr("disabled");
	} else {
		$("#btn-redo").attr("disabled", "disabled");
	}

}

function doUndo() {
	if (undoStack.length>0) {
		var undoStep=undoStack.pop();
		var changes = {
			cells: []
		};
		if (undoStep.shiftChange) {
			var dir=undoStep.shiftChange.dir;
			if (dir=='left') {
				gridArtwork.doShiftRight(grid);
				changes.shift = 'right';
			} else if (dir=='right') {
				gridArtwork.doShiftLeft(grid);
				changes.shift = 'left';
			} else if (dir=='up') {
				gridArtwork.doShiftDown(grid);
				changes.shift = 'down';
			} else if (dir=='down') {
				gridArtwork.doShiftUp(grid);
				changes.shift = 'up';
			}
			var removedCells=undoStep.shiftChange.removedCells;
			for (var i=0; i<removedCells.length; i++) {
				paintOnCanvas(
					removedCells[i].col, 
					removedCells[i].row, 
					removedCells[i].shapeName, 
					removedCells[i].color);
				changes.cells.push({
					col: removedCells[i].col,
					row: removedCells[i].row,
					shapeName: removedCells[i].shapeName,
					color: removedCells[i].color
				});
			}
		} else if (undoStep.backgroundChange) {
			setBackgroundColor(undoStep.backgroundChange.oldColor);
			changes.backgroundColor = undoStep.backgroundChange.oldColor
		} else if (undoStep.workspaceChange) {
			applyWorkspaceSize(
				undoStep.workspaceChange.oldWorkspace.width,
				undoStep.workspaceChange.oldWorkspace.height,
				undoStep.workspaceChange.oldWorkspace.cellSize,
				undoStep.workspaceChange.oldWorkspace.gridThickness,
				undoStep.workspaceChange.oldWorkspace.gridColor,
				undoStep.workspaceChange.oldWorkspace.backgroundColor
			);
			changes.workspace = undoStep.workspaceChange.oldWorkspace;
		} else {
			for (var i=0; i<undoStep.cellChanges.length; i++) {
				cc=undoStep.cellChanges[i];
				paintOnCanvas(cc.col, cc.row, cc.oldShapeName, cc.oldColor);
				changes.cells.push({
					col: cc.col,
					row: cc.row,
					shapeName: cc.oldShapeName,
					color: cc.oldColor
				})
			}			
		}
		
		redoStack.push(undoStep);
		updateUndoRedoButtons();

		if (socket) {
			console.log('socket.io <- changes (undo)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}
}

function doRedo() {
	if (redoStack.length>0) {
		var redoStep=redoStack.pop();
		var changes = {
			cells: []
		}
		if (redoStep.shiftChange) {
			var dir=redoStep.shiftChange.dir;
			if (dir=='left') {
				gridArtwork.doShiftLeft(grid);
				changes.shift = 'left';
			} else if (dir=='right') {
				gridArtwork.doShiftRight(grid);
				changes.shift = 'right';
			} else if (dir=='up') {
				gridArtwork.doShiftUp(grid);
				changes.shift = 'up';
			} else if (dir=='down') {
				gridArtwork.doShiftDown(grid);
				changes.shift = 'down'
			}
		} else if (redoStep.backgroundChange) {
			setBackgroundColor(redoStep.backgroundChange.newColor);	
			changes.backgroundColor = redoStep.backgroundChange.newColor;
		} else if (redoStep.workspaceChange) {
			applyWorkspaceSize(
				undoStep.workspaceChange.newWorkspace.width,
				undoStep.workspaceChange.newWorkspace.height,
				undoStep.workspaceChange.newWorkspace.cellSize,
				undoStep.workspaceChange.newWorkspace.gridThickness,
				undoStep.workspaceChange.newWorkspace.gridColor,
				undoStep.workspaceChange.newWorkspace.backgroundColor
			);
			changes.workspace = undoStep.workspaceChange.newWorkspace;
		} else {
			for (var i=0; i<redoStep.cellChanges.length; i++) {
				cc=redoStep.cellChanges[i];
				paintOnCanvas(cc.col, cc.row, cc.newShapeName, cc.newColor);
				changes.cells.push({
					col: cc.col,
					row: cc.row,
					shapeName: cc.newShapeName,
					color: cc.newColor
				})
			}
		}
		
		undoStack.push(redoStep);
		updateUndoRedoButtons();

		if (socket) {
			console.log('socket.io <- changes (redo)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}	
}

function pasteSelection() {
	var pasteCells=selection.getPasteCells();
	for (var i=0; i<pasteCells.length; i++) {
		var cc=pasteCells[i];
		storeUndoCell(cc.col, cc.row, cc.shapeName, cc.color);
		paintOnCanvas(cc.col, cc.row, cc.shapeName, cc.color);
	}
	changed=true;

	if (socket != null) {
		var changes = {
			cells: pasteCells
		}
		console.log('socket.io <- changes (pasteSelection)');
		console.log(changes);
		socket.emit('changes', changes);
	}
}

function setBackgroundColor(color) {
	backgroundColor=color;
	$("#canvas").css("background-color",backgroundColor);
}

function showWarningMessage(message) {
	var messageModal=$("#message-modal");
	messageModal.find("#message-text").text(message);
	messageModal.modal();
}

function showCircleLoader() {
	$('body').append(
		'<div id="spinner-fullscreen" class="spinner-fillscreen-wrapper"><div class="spinner wide"></div></div>'
	)
}

function hideCircleLoader() {
	$('#spinner-fullscreen').remove();
}

function initPropertiesDialog() {
	$("#btn-properties-save").click(
		function() {
			var artworkName=$("#modal_artwork_name").val();
			if (artworkName=="") {
				var messageModal=$("#message-modal");
				messageModal.find("#message-text").text("Please enter artwork name");
				messageModal.modal();
				return;
			}
						
			$("#artwork_name").val($("#modal_artwork_name").val());
			$("#artwork_tags").val($("#modal_artwork_tags").val());
			$("#artwork_description").val($("#modal_artwork_description").val());

			$("#properties-modal").modal('hide');
			
			var modalAction=$("#modal_success_action").val();
			if (modalAction=="save") {
				saveArtwork();
			}
		}
	);

	initialTagsValue = $('input[name=modal_artwork_tags]').val();

	var tags=$("#modal_artwork_tags");
	tags.tagsinput();
	tags.tagsinput('input').typeahead({
		name: "dataset",
		remote: "/tag-typeahead?query=%QUERY"
    }).bind('typeahead:selected', $.proxy(function (obj, datum) {
      tags.tagsinput('add', datum.value);
      tags.tagsinput('input').typeahead('setQuery', '');
    }, $('input')));
	tags.on(
		'beforeItemAdd',
		function(event) {
			if (event.item.length <= 1 || event.item.length > 64) {
				$("#modal-tags-hint").show();
				event.cancel = true
			} else {
				$("#modal-tags-hint").hide();
			}
		}
	);

	$('#modal_description_label').click(function() {
		if (modalDescriptionVisible) {
			$('#modal_description_label i').removeClass('icon-caret-down').addClass('icon-caret-right');
			$('#modal_artwork_description').hide();
			propertiesDialog_updateDescriptionLabelPreview();
			$('#modal_description_label').find('.save-dialog-expandable-content-preview').show();
			modalDescriptionVisible=false;			
		} else {
			$('#modal_description_label i').removeClass('icon-caret-right').addClass('icon-caret-down');
			$('#modal_artwork_description').show();
			$('#modal_description_label').find('.save-dialog-expandable-content-preview').hide();
			modalDescriptionVisible=true;
		}
	});
	
	$('#modal_tags_label').click(function() {
		if (modalTagsVisible) {
			$('#modal_tags_label i').removeClass('icon-caret-down').addClass('icon-caret-right');
			$('#modal_artwork_tags_field').hide();
			$('#modal-tags-hint').hide();
			propertiesDialog_updateTagsLabelPreview();
			$('#modal_tags_label').find('.save-dialog-expandable-content-preview').show();
			modalTagsVisible=false;
		} else {
			$('#modal_tags_label i').removeClass('icon-caret-right').addClass('icon-caret-down');
			$('#modal_artwork_tags_field').show();
			$('#modal_tags_label').find('.save-dialog-expandable-content-preview').hide();
			modalTagsVisible=true;			
		}
	});
	
	$('#modal_square_grid_special_properties_label').click(function() {
		if (modalSquareGridSpecialPropertiesVisible) {
			$('#modal_square_grid_special_properties_label i').removeClass('icon-caret-down').addClass('icon-caret-right');
			$('.save-dialog-special-properties-frame').hide();
			modalSquareGridSpecialPropertiesVisible=false;
		} else {
			$('#modal_square_grid_special_properties_label i').removeClass('icon-caret-right').addClass('icon-caret-down');
			$('.save-dialog-special-properties-frame').show();
			modalSquareGridSpecialPropertiesVisible=true;			
		}
	});

	$('#properties-modal').on('shown.bs.modal', function () {
		$('#modal_artwork_name').focus();
	});
}

function initShiftPanel() {
	$("#shift-toolbar-header").click(
		function() {
			if ($(this).attr("content-visible")) {
				$("#shift-toolbar-content").slideUp();
				$("#shift-toolbar-header i").removeClass("icon-chevron-up");
				$("#shift-toolbar-header i").addClass("icon-chevron-down");
				$(this).removeAttr("content-visible");
			} else {
				$("#shift-toolbar-content").slideDown();
				$("#shift-toolbar-header i").removeClass("icon-chevron-down");
				$("#shift-toolbar-header i").addClass("icon-chevron-up");
				$(this).attr("content-visible","visible");				
			}
		});

	var sendShiftBySocket = function(shift) {
		if (socket) {
			var changes = {
				shift: shift
			}
	
			console.log('socket.io <- changes (shiftWorkspace)');
			console.log(changes);
			socket.emit('changes', changes);
		}
	}

	$("#btn-shift-left").click(
		function() {
			removedCells=gridArtwork.doShiftLeft(grid);
			changed=true;
			
			undoStep=new UndoStep();
			undoStep.setShiftChange('left', removedCells);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();
			sendShiftBySocket('left');
		});
	
	$("#btn-shift-right").click(
		function() {
			removedCells=gridArtwork.doShiftRight(grid);
			changed=true;
			
			undoStep=new UndoStep();
			undoStep.setShiftChange('right', removedCells);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();
			sendShiftBySocket('right');
		});
		
	$("#btn-shift-up").click(
		function() {
			removedCells=gridArtwork.doShiftUp(grid);
			changed=true;
			
			undoStep=new UndoStep();
			undoStep.setShiftChange('up', removedCells);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();
			sendShiftBySocket('up');
		});
		
	$("#btn-shift-down").click(
		function() {
			removedCells=gridArtwork.doShiftDown(grid);
			changed=true;
			
			undoStep=new UndoStep();
			undoStep.setShiftChange('down', removedCells);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();
			sendShiftBySocket('down');
		});
}

function applyWorkspaceSize(newWidth, newHeight, newCellSize, gridThickness, gridColor, backgroundColor) {
	$("#canvas")
		.css("width",newWidth)
		.css("height",newHeight);
	grid.workspaceWidth=newWidth;
	grid.workspaceHeight=newHeight;
	grid.cellSize=newCellSize;
	grid.gridThickness=gridThickness;
	grid.gridColor=gridColor;
	
	paper.remove();
	paper=new Raphael("canvas",newWidth,newHeight);
	grid.paintGrid(paper);
	selection.paper=paper;

	setBackgroundColor(backgroundColor);
	
	var oldGridArtwork=gridArtwork;
	gridArtwork=new GridArtwork();
	for (var row=0; row<oldGridArtwork.cells.length; row++) {
		for (var col=0; col<oldGridArtwork.cells[row].length; col++) {
			var cell=oldGridArtwork.cells[row][col];
			if (cell) {
				var cellRect=grid.getCellRect(col,row);
				if (cellRect.left+cellRect.width<newWidth && cellRect.top+cellRect.height<newHeight) {
					paintOnCanvas(col,row,cell.shapeName,cell.color);
				}
			}
		}
	}

	$("#workspace-width").val(newWidth);
	$("#workspace-height").val(newHeight);
	$("#workspace-cell-size").val(newCellSize);
	$("#workspace-grid-thickness").val(gridThickness);
	$("#workspace-grid-color").minicolors("value", gridColor);
	$("#workspace-background-color").minicolors("value", backgroundColor);
}

function initSizePanel() {
	$("#size-toolbar-header").click(
		function() {
			if ($(this).attr("content-visible")) {
				$("#size-toolbar-content").slideUp();
				$("#size-toolbar-header i").removeClass("icon-chevron-up");
				$("#size-toolbar-header i").addClass("icon-chevron-down");
				$(this).removeAttr("content-visible");
			} else {
				$("#size-toolbar-content").slideDown();
				$("#size-toolbar-header i").removeClass("icon-chevron-down");
				$("#size-toolbar-header i").addClass("icon-chevron-up");
				$(this).attr("content-visible","visible");				
			}
		});

	$("#btn-set-workspace-size").click(
		function() {
			// !!!!!
			var newWidth=parseInt($("#workspace-width").val(),10);
			var newHeight=parseInt($("#workspace-height").val(),10);
			var newCellSize=parseInt($("#workspace-cell-size").val(),10);
			var newGridThickness=parseInt($("#workspace-grid-thickness").val(),10);
			var newGridColor=$("#workspace-grid-color").val();
			var newBackgroundColor=$("#workspace-background-color").val();

			undoStep=new UndoStep();
			undoStep.setWorkspaceChange(
				{
					width: grid.workspaceWidth,
					height: grid.workspaceHeight,
					cellSize: grid.cellSize,
					gridThickness: grid.gridThickness,
					gridColor: grid.gridColor,
					backgroundColor: backgroundColor
				},
				{
					width: newWidth,
					height: newHeight,
					cellSize: newCellSize,
					gridThickness: newGridThickness,
					gridColor: newGridColor,
					backgroundColor: newBackgroundColor
				}
			);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();

			
			if (newWidth<200 || newWidth>4000) {
				alert("Artwork width should by between 200 and 4000 pixels.");
				return;
			}
			
			if (newHeight<200 || newHeight>4000) {
				alert("Artwork height should be between 200 and 4000 pixels");
				return;
			}
			
			if (newCellSize<10 || newCellSize>32) {
				alert("Cell size should be between 10 and 32 pixels");
				return;
			}

			if (newGridThickness<1 || newGridThickness>4) {
				alert("Grid thickness should be between 1 and 4 pixels");
				return;
			}

			applyWorkspaceSize(newWidth, newHeight, newCellSize, newGridThickness, newGridColor, newBackgroundColor);

			$("#workspace-size-modal").modal("hide");

			if (socket) {
				var changes = {
					workspace: {
						width: newWidth,
						height: newHeight,
						cellSize: newCellSize,
						gridThickness: newGridThickness,
						gridColor: newGridColor,
						backgroundColor: newBackgroundColor
					}
				}
		
				console.log('socket.io <- changes (setWorkspaceSize)');
				console.log(changes);
				socket.emit('changes', changes);
			}
		});
}

function initCopyPastePanel() {
	$("#copy-paste-toolbar-header").click(
		function() {
			if ($(this).attr("content-visible")) {
				$("#copy-paste-toolbar-content").slideUp();
				$("#copy-paste-toolbar-header i").removeClass("icon-chevron-up");
				$("#copy-paste-toolbar-header i").addClass("icon-chevron-down");
				$(this).removeAttr("content-visible");
			} else {
				$("#copy-paste-toolbar-content").slideDown();
				$("#copy-paste-toolbar-header i").removeClass("icon-chevron-down");
				$("#copy-paste-toolbar-header i").addClass("icon-chevron-up");
				$(this).attr("content-visible","visible");
				if (!localStorage["dontShowCopyPasteMessage"]) {
					$("#copy-paste-message-modal").modal();	
				}
			}
		});

	$("#btn-copy-mode").click(
		function(event) {
			if (mode=="copy") {
				setMode("paint");
			} else {
				setMode("copy");
			} 
		});
	
	$("#btn-paste-mode").click(
		function(event) {
			if (mode=="paste") {
				setMode("paint");
			} else {
				setMode("paste");
			} 
		});
	
}

function initDrawingToolsPanel() {
	$("#btn-pick-color").click(function() {
		setMode("pick-color");
	});
	
	$('#btn-pencil').click(function() {
		setMode('paint');
	});

	$('#btn-erase').click(function() {
		setMode('erase');
	})

	$("#btn-flood-fill").click(function() {
		setMode('fill');
	});

	if (grid.getAdjacentCells && grid.isCellInsideWorkspace) {
		$('#btn-flood-fill').show();
	}

	if (grid.drawTools) {
		for (var toolName in grid.drawTools) {
			var tool = grid.drawTools[toolName];
			var button = $(`<button class="btn btn-sm btn-default painter-btn-tool btn-draw-tool" type="button" tool-name="${toolName}" title="${tool.title}"><img src="${tool.iconUrl}" /></button>`)
			$('#draw-tools-bar').append(button);
		}
		$('.btn-draw-tool').click(function(event) {
			var toolName = $(this).attr('tool-name');
			setMode(toolName);
		});
	}	
}

function initShapesToolbar() {
	shapesToolbarGrid = gridFactory[artwork.layers[0].grid]();
	shapesToolbarGrid.cellSize = 24; // TODO toolbar cell size from grid defaults

	var shapeElements="";
	for(var i = 0; i < shapesToolbarGrid.shapesToolbar.length; i++) {
		shapeElements += '<div class="shapes-toolbar-row" id="shapes-toolbar-row-' + i +'">';
		for (var j = 0; j < shapesToolbarGrid.shapesToolbar[i].length; j++) {
			var shapeName = shapesToolbarGrid.shapesToolbar[i][j];
			shapeElements += '<span id="shape-' + shapeName +
				'" class="grid-shape-button" shape-name="' +
				shapeName+'"></span>';
		}
		shapeElements += '</div>';	
	}

	$("#shapes-toolbar").html(shapeElements);
	
	selectedShapeName="flat";
	for (var shapeName in shapesToolbarGrid.shapes) {
		paintShapeToolButton(shapeName);
	}
	
	$(".grid-shape-button").click(
		function() {
			selectShape($(this).attr("shape-name"));
		}
	);

	if (shapesToolbarGrid.shapesToolbar.length <= 2) {
		$("#shapes-toolbar-header i").hide();
	} else {
		for(var i = 2; i < shapesToolbarGrid.shapesToolbar.length; i++) {
			$('#shapes-toolbar-row-' + i).hide();
		}

		$("#shapes-toolbar-header").click(function() {
			if ($(this).attr("content-visible")) {
				var selectedRowIndex = 1;
				for(var i = 2; i < shapesToolbarGrid.shapesToolbar.length; i++) {
					if (shapesToolbarGrid.shapesToolbar[i].includes(selectedShapeName)) {
						selectedRowIndex = i;
						break;
					}
				}
				for(var i = 1; i < shapesToolbarGrid.shapesToolbar.length; i++) {
					if (i != selectedRowIndex) {
						$('#shapes-toolbar-row-' + i).slideUp();
					}
				}
				$("#shapes-toolbar-header i").removeClass("icon-chevron-up");
				$("#shapes-toolbar-header i").addClass("icon-chevron-down");
				$(this).removeAttr("content-visible");
			} else {
				for(var i = 0; i < shapesToolbarGrid.shapesToolbar.length; i++) {
					$('#shapes-toolbar-row-' + i).slideDown();
				}
				$("#shapes-toolbar-header i").removeClass("icon-chevron-down");
				$("#shapes-toolbar-header i").addClass("icon-chevron-up");
				$(this).attr("content-visible","visible");
			}
		});
	}
}

function onCanvasMouseDown(event) {
	paperMouseDown=true;
	updateCellCoordiantesPanel(event);
	
	if (mode=="paint") {
		undoStack.push(new UndoStep());
		redoStack=[];
		updateUndoRedoButtons();
		paintOnCanvasByMouseEvent(event);
	} else if (mode=='erase') {
		undoStack.push(new UndoStep());
		redoStack=[];
		updateUndoRedoButtons();
		eraseOnCanvasByMouseEvent(event);
	} else if (mode=="pick-color") {
		pickColorByMouseEvent(event);
	} else if (mode=="copy") {
		selectOnCanvasByMouseEvent(event);
	} else if (mode=="paste") {
		undoStack.push(new UndoStep());
		redoStack=[];
		updateUndoRedoButtons();
		pasteSelection();
		selection.pasteFinished();
	} else if (mode=='fill') {
		undoStack.push(new UndoStep());
		redoStack=[];
		updateUndoRedoButtons();
		fillAreaOnCanvasByMouseEvent(event);
	} else if (grid.drawTools && grid.drawTools[mode]) {
		undoStack.push(new UndoStep());
		redoStack=[];
		updateUndoRedoButtons();
		draftDrawToolOnCanvasByMouseEvent(event)
	}
}

function onCanvasMouseUp(event) {
	paperMouseDown=false;
			
	if (mode=="paste") {
		setMode("paint");
	} else if (grid.drawTools && grid.drawTools[mode]) {
		drawToolOnCanvas();
	}
}

function onCanvasMouseMove(event) {
	updateCellCoordiantesPanel(event);
	if (mode=="paint") {
		paintOnCanvasByMouseEvent(event);
	} else if (mode=='erase') {
		eraseOnCanvasByMouseEvent(event);
	} else if (mode=="copy") {
		selectOnCanvasByMouseEvent(event);
	} else if (mode=="paste") {
		changePastePositionByMouseEvent(event);
	} else if (grid.drawTools && grid.drawTools[mode]) {
		draftDrawToolOnCanvasByMouseEvent(event);
	}
}

function is_touch_device() {  
	try {  
	  	document.createEvent("TouchEvent");  
	  	return true;  
	} catch (e) {  
	  	return false;  
	}  
}

var touchMode = 'ready';
var touchDown = false;
var ongoingTouches = new Array();

function getOngoingTouch(identifier) {
	for (let i = 0; i < ongoingTouches.length; i++) {
		if (ongoingTouches[i].identifier == identifier) {
			return ongoingTouches[i];
		}
	}
}

function setOngoingTouch(identifier, pageX, pageY) {
	for (let i = 0; i < ongoingTouches.length; i++) {
		if (ongoingTouches[i].identifier == identifier) {
			ongoingTouches[i].pageX = pageX;
			ongoingTouches[i].pageY = pageY;
			return;
		}
	}
	ongoingTouches.push({
		identifier: identifier,
		pageX: pageX,
		pageY: pageY
	});
}

function deleteOngoingTouch(identifier) {
	let index = -1;
	for (let i = 0; i < ongoingTouches.length; i++) {
		if (ongoingTouches[i] == identifier) {
			index = i;
			break;
		}
	}
	ongoingTouches.splice(index, 1);
}

function onCanvasTouchStart(evt) {
	evt.preventDefault();
	let touches = evt.originalEvent.changedTouches;
	for (let i = 0; i < touches.length; i++) {
		setOngoingTouch(touches[i].identifier, touches[i].pageX, touches[i].pageY);
	}

	if (touchMode == 'ready') {
		if (ongoingTouches.length == 1) {
			touchMode = 'paint'
		} else if (ongoingTouches.length == 2) {
			touchMode = 'pan'
		} else {
			touchMode = 'invalid';
		}
	} else if (touchMode == 'paint') {
		if (ongoingTouches.length == 1) {
		}
		else if (ongoingTouches.length == 2) {
			touchMode = 'pan'
		} else {
			touchMode = 'invalid'
		}
	}
}

function onCanvasTouchMove(evt) {
	evt.preventDefault();

	if (touchMode == 'paint') {
		let currentTouch = evt.originalEvent.changedTouches[0];
		let prevTouch = getOngoingTouch(currentTouch.identifier);
		if (!prevTouch) {
			console.log('no prev touch', currentTouch.identifier, ongoingTouches);
			return;
		}
		if (Math.abs(currentTouch.pageX - prevTouch.pageX) < 4 && Math.abs(currentTouch.pageY - prevTouch.pageY) < 4) {
			console.log('no move');
			return;
		}
		let mouseEvent = {
			pageX: currentTouch.pageX,
			pageY: currentTouch.pageY,
			which: 1,
			altKey: evt.altKey,
			ctrlKey: evt.ctrlKey,
			shiftKey: evt.shiftKey
		}
		if (!touchDown) {
			onCanvasMouseDown(mouseEvent)
			touchDown = true;
		}
		onCanvasMouseMove(mouseEvent);
		setOngoingTouch(currentTouch.identifier, currentTouch.pageX, currentTouch.pageY);
	} else if (touchMode == 'pan' && evt.originalEvent.changedTouches.length == 2 && ongoingTouches.length == 2) {
		let newTouches = evt.originalEvent.changedTouches;
		let newTouch_1 = newTouches[0];
		let newTouch_2 = newTouches[1];
		let oldTouch_1 = getOngoingTouch(newTouch_1.identifier);
		let oldTouch_2 = getOngoingTouch(newTouch_2.identifier);
		let dx1 = newTouch_1.pageX - oldTouch_1.pageX;
		let dy1 = newTouch_1.pageY - oldTouch_1.pageY;
		let dx2 = newTouch_2.pageX - oldTouch_2.pageX;
		let dy2 = newTouch_2.pageY - oldTouch_2.pageY;
		let scalarMult = dx1 * dx2 + dy1 * dy2;
		if (scalarMult > 0) {
			let dx = (dx1 + dx2) / 2;
			let dy = (dy1 + dy2) / 2
			try {
				$('#canvas').parent()[0].scrollBy(-dx, -dy);
			} catch (e) {
				console.log(e);
			}
		}
		setOngoingTouch(newTouch_1.identifier, newTouch_1.pageX, newTouch_1.pageY);
		setOngoingTouch(newTouch_2.identifier, newTouch_2.pageX, newTouch_2.pageY);
	}
}

function onCanvasTouchEnd(evt) {
	evt.preventDefault();
	let touches = evt.originalEvent.changedTouches;
	if (touchMode == 'paint' && touches.length == 1) {
		if (touchDown) {
			let mouseEvent = {
				pageX: touches[0].pageX,
				pageY: touches[0].pageY,
				which: 1,
				altKey: evt.altKey,
				ctrlKey: evt.ctrlKey,
				shiftKey: evt.shiftKey
			}			
			onCanvasMouseMove(mouseEvent);
			onCanvasMouseUp(mouseEvent);
		}
	}

	for (let i = 0; i < touches.length; i++) {
		deleteOngoingTouch(touches[i].identifier);
	}

	touchDown = false;
	if (ongoingTouches.length == 0) {
		touchMode = 'ready';
	} else {
		touchMode = 'invalid';
	}
}

function onCanvasTouchCancel(evt) {
	onCanvasTouchEnd(evt)
}

function addCollaborator(collaborator) {
    var sid = collaborator.sid;
    var exists = false;
    for (var i = 0; i < collaboratorsOnline.length; i++) {
        if (collaboratorsOnline[i].sid == sid) {
            exists = true;
            break;
        }
	}
	if (!exists) {
		collaboratorsOnline.push(collaborator);
	}
}

function deleteCollaborator(sid) {
    var index = -1;
    for (var i = 0; i < collaboratorsOnline.length; i++) {
        if (collaboratorsOnline[i].sid == sid) {
            index = i
            break;
        }
	}
	collaboratorsOnline.splice(index, 1);
}

function updateCollaboratorsPanel() {
    if (collaboratorsOnline.length == 0) {
        $('.group-image-users-online').hide();
        $('#call-collaborators').show();
        return;
    } else {
        $('.group-image-users-online').show();
        $('#call-collaborators').hide();
    }
    var html = '';
    for (var i = 0; i < collaboratorsOnline.length; i++) {
        var c = collaboratorsOnline[i]
        html += `<div class="user-icon" style="background-image: url(${c.user.avatar_url})" title="${c.user.nickname}"></div>`;
    }
    $('.group-image-users-online').html(html);
}

function sendMessageToChat() {
	if (!socket) {
		return;
	}

	let text = $('#group-image-chat-input').val().trim();
	$('#group-image-chat-input').val('');
	if (text=='') {
		return;
	}

	console.log('socket.io <- add_chat_message')
	socket.emit('add_chat_message', {text: text})
}

function safe_tags(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') ;
}


var lastChatMessageUserId = null;
var chatWindowVisible = false;

function showChatMessage(chat_message) {
	let tokenPayload = JSON.parse(atob(exchangeToken.split('.')[1]));
	let currentUser = tokenPayload.user;
	let messageClass = 'other-user'
	if (chat_message.user.user_id == currentUser.user_id) {
		messageClass = 'current-user'
	}

	let messageHtml = null;
	if (lastChatMessageUserId == chat_message.user.user_id) {
		messageHtml = `
			<div class="group-image-chat-message ${messageClass}">
				<div class="chat-message-content">
					<div class="chat-message-text">
						${chat_message.text}
					</div>
				</div>
			</div>`;
	} else {
		messageHtml = `
			<div class="group-image-chat-message ${messageClass}">
				<div class="chat-message-avatar" style="background-image: url(${chat_message.user.avatar_url})"></div>
				<div class="chat-message-content">
					<div class="chat-message-author">${safe_tags(chat_message.user.nickname)}</div>
					<div class="chat-message-text">
						${safe_tags(chat_message.text)}
					</div>
				</div>
			</div>`;
	}
	$('.group-image-chat-messages-list').append(messageHtml);
	$('.group-image-chat-messages-container').animate({scrollTop: $('.group-image-chat-messages-list').height()}, 300);
	showChatWindow();

	lastChatMessageUserId = chat_message.user.user_id;
}

function showChatWindow() {
	$('.group-image-chat-show-button').html('<i class="glyphicon glyphicon-chevron-down"></i>').show();
	$('.group-image-chat-messages').slideDown();
	chatWindowVisible = true;
}

function hideChatWindow() {
	$('.group-image-chat-show-button').html('<i class="glyphicon glyphicon-chevron-up"></i>')
	$('.group-image-chat-messages').slideUp();
	chatWindowVisible = false;
}

function toggleChatWindow() {
	if (chatWindowVisible) {
		hideChatWindow();
	} else {
		showChatWindow();
	}
}


var initComplete = false;
function initialPaintArtwork() {
    initComplete = true;
    hideCircleLoader();
    if (artwork.version.major==1) {
		var layer=artwork.layers[0];
		for (var i=0; i<layer.cells.length; i++) {
			paintOnCanvas(layer.cells[i].col, layer.cells[i].row, layer.cells[i].shape, layer.cells[i].color);
		}
	} else if (artwork.version.major==2) {
		var layer=artwork.layers[0];
		for (var rowIndex=0; rowIndex<layer.rows.length; rowIndex++) {
			var cellRow=layer.rows[rowIndex];
			for (var cellIndex=0; cellIndex<cellRow.cells.length; cellIndex++) {
				var cell=cellRow.cells[cellIndex];
				paintOnCanvas(cell[0], cellRow.row, cell[1], cell[2]);
			}
		}
	}
}


function drawCollaboratorPointerToCell(user, cell) {
	var item = null;
	var pointer = $('#collaborator-pointer-' + user.user_id)
	var cellRect = grid.getCellRect(cell.col, cell.row);
	var x = cellRect.left + cellRect.width / 2;
	var y = cellRect.top + cellRect.height / 2;

	if (pointer.length == 0) {
		html = 
			`<div class="collaborator-pointer" id="collaborator-pointer-${user.user_id}">
				<div class="wrapper">				
					<div class="arrow"></div>
					<div class="nickname">${user.nickname}</div>
					<div class="avatar" style="background-image: url(${user.avatar_url})"></div>
				</div>
			</div>`;
		pointer = $(html);
		console.log(pointer);
		$('#canvas-wrapper #canvas').append(pointer);
	}

	pointer.css('left', (x - 10) + 'px');
	pointer.css('top', (y - 30) + 'px');
	pointer.show();
}


$(function() {
	adjustCanvasWrapper();
	$(window).resize(
		function() {
			adjustCanvasWrapper();
		});
			
	backgroundColor=artwork.backgroundColor;
	$("#canvas")
		.css("background-color",backgroundColor)
		.css("width",artwork.canvasSize.width)
		.css("height",artwork.canvasSize.height);
		
	paper=new Raphael("canvas",artwork.canvasSize.width,artwork.canvasSize.height);
	grid=gridFactory[artwork.layers[0].grid]();
	grid.cellSize=artwork.layers[0].cellSize;
	grid.workspaceWidth=artwork.canvasSize.width;
	grid.workspaceHeight=artwork.canvasSize.height;
	grid.gridThickness=artwork.layers[0].gridThickness ? artwork.layers[0].gridThickness : 1;
	grid.gridColor=artwork.layers[0].gridColor ? artwork.layers[0].gridColor : "#d0d0d0";
	grid.paintGrid(paper);
	
	selection.grid=grid;
	selection.paper=paper;
	selection.loadFromLocalStorage();
	
	initShapesToolbar();
	updateUndoRedoButtons();
	
	$("#workspace-width").val(artwork.canvasSize.width);
	$("#workspace-height").val(artwork.canvasSize.height);
	$("#workspace-cell-size").val(artwork.layers[0].cellSize);
	if (artwork.layers[0].gridThickness) {
		$("#workspace-grid-thickness").val(artwork.layers[0].gridThickness);
	} else {
		$("#workspace-grid-thickness").val("1");
	}
	if (artwork.layers[0].gridColor) {
		$("#workspace-grid-color").val(artwork.layers[0].gridColor);
	} else {
		$("#workspace-grid-color").val("#d0d0d0");
	}
	$("#workspace-background-color").val(artwork.backgroundColor);
	
	$('#modal_artwork_grid_visible')[0].checked = artwork['gridVisible'];
	$('#modal_artwork_pixel_art')[0].checked = artwork['additionalPixelImage'];
	$('#modal_transparent_background')[0].checked = artwork['transparentBackground'];

	$("#canvas")
		.mousedown(onCanvasMouseDown)
		.mouseup(onCanvasMouseUp)
		.mousemove(onCanvasMouseMove);

	if (is_touch_device()) {
		console.log('Touch present');
		$("#canvas")
			.on('touchstart', onCanvasTouchStart)
			.on('touchmove', onCanvasTouchMove)
			.on('touchend', onCanvasTouchEnd)
			.on('touchcancel', onCanvasTouchCancel)
	}
	
	$.mask.definitions['k'] = "[A-Fa-f0-9]";
	$("#color-picker-text").mask("#kkkkkk");
	$("#color-picker-text").change(
		function() {
			selectColorFromText($(this).val());
		}
	).keyup(
		function() {
			selectColorFromText($(this).val());
		}
	);
	
	$("#color-picker").minicolors({
		inline:true,
		control: "brightness",
		change: function(hex,opacity) {
			selectColorFromPicker(hex);
		}
	}).minicolors("value",selectedColor);

	$("#workspace-grid-color").minicolors({
		theme: 'bootstrap',
		letterCase: 'uppercase',
	});

	$("#workspace-background-color").minicolors({
		theme: 'bootstrap',
		letterCase: 'uppercase',
	});

	$("#btn-set-background-color").click(
		function() {
			undoStep=new UndoStep();
			undoStep.setBackgroundChange(backgroundColor, selectedColor);
			undoStack.push(undoStep);
			redoStack=[];
			updateUndoRedoButtons();
			
			setBackgroundColor(selectedColor);

			if (socket) {
				var changes = {
					backgroundColor: selectedColor
				}
		
				console.log('socket.io <- changes (setBackgroundColor)');
				console.log(changes);
				socket.emit('changes', changes);
			}
		}
	);
	
	$("#btn-save").click(
		function() {
			showPropertiesDialog("save");
		}
	);

	$("#btn-workspace-size").click(
		function() {
			$("#workspace-size-modal").modal("show");
		}
	)
		
	window.onbeforeunload=
		function() {
			if (changed) {
				return "Your drawing was changed. Do you want to leave without saving?";
			}
		};		
	
	//Create color palette
	var paletteHtml="";
	for (var i=0; i<22; i++) {
		paletteHtml+="<div></div>";
		recentColors.push("#FFFFFF");
	}
	$("#color-palette").html(paletteHtml);
	$("#color-palette div").click(
		function() {
			hexColor=rgb2hex($(this).css("background-color"));
			$("#color-picker").minicolors("value",hexColor);
			//selectColor(hexColor);
		}
	);
	
	//Fill color palette with recent colors
	if (artwork.recentColors) {
		$paletteDivs=$("#color-palette div");
		for (var i=0; i<$paletteDivs.length && i<artwork.recentColors.length; i++) {
			$($paletteDivs[i]).css("background-color",artwork.recentColors[i]);
			recentColors[i]=artwork.recentColors[i];
		}	
	}
	selectColor(recentColors[0]);
		
	setMode("paint");
		
	$("#btn-undo").click(
		function() {
			doUndo();
		});
		
	$("#btn-redo").click(
		function() {
			doRedo();
		});
									
	//Disable context menu on canvas
	$("#canvas").bind("contextmenu", 
		function(e) {
    		return false;
		});
	
	$("body").keydown(
		function(event) {
			if (event.ctrlKey && event.keyCode==90) {
				//Ctrl-Z
				doUndo();
			}
		});
						
	$("#copy-paste-message-modal").on("hidden.bs.modal",
		function() {
			if ($("#chk-dont-show-copy-paste-message")[0].checked) {
				localStorage['dontShowCopyPasteMessage']=true;
			}
		});

	initPropertiesDialog();
	initDrawingToolsPanel();
	initShiftPanel();
	initSizePanel();
	initCopyPastePanel();

	if (exchangeToken) {
		$('.group-image-online').show();
		
		$('#btn-send-message-to-chat').click(sendMessageToChat);
		$('#group-image-chat-input').on('keypress',function(e) {
			if(e.which == 13) {
				sendMessageToChat();
			}
		});
		$('.group-image-chat-show-button').click(toggleChatWindow);

	    showCircleLoader();
	    timeoutTaskId = setTimeout(initialPaintArtwork, 5000)

	    socket = io(exchangeUrl);
	    socket.on('connect', (data) => {
			console.log('socket.io => connect');
	        console.log('socket.io <- login');
	        socket.emit('login', {'token': exchangeToken})
            $('#socketio-online').show();
			$('#call-collaborators').show();
			$('#group-image-chat-wrapper').show();
            $('#socketio-offline').hide();
	    });
	    socket.on('disconnect', (data) => {
	        console.log('socket.io => disconnect');
            $('#socketio-online').hide();
			$('#call-collaborators').hide();
			$('#group-image-chat-wrapper').hide();
			$('#socketio-offline').show();
			collaboratorsOnline = [];
			updateCollaboratorsPanel();
	    })
	    socket.on('login_ok', (data) => {
	        console.log('socket.io => login_ok');

	        var tokenPayload = JSON.parse(atob(exchangeToken.split('.')[1]));
	        console.log('socket.io <- hello');
	        console.log(tokenPayload.user);
	        socket.emit('hello', tokenPayload.user);

	        console.log('socket.io <- who_is_here')
	        socket.emit('who_is_here', {})
	    });
	    socket.on('login_fail', (data) => {
	        console.log('socket.io => login_fail');
	    });
	    socket.on('you_are_first', (data) => {
	        console.log('socket.io => you_are_first')
	        if (!initComplete) {
	            clearTimeout(timeoutTaskId);
	            initialPaintArtwork();
	        }
	    });
	    socket.on('hello', (data) => {
	        console.log('socket.io => hello');
	        console.log(data);
	        addCollaborator(data);
	        updateCollaboratorsPanel();
	    });
	    socket.on('bye', (data) => {
	        console.log('socket.io => bye');
	        console.log(data)
	        var sid = data.sid;
	        deleteCollaborator(sid);
	        updateCollaboratorsPanel();
	    });
	    socket.on('who_is_here', (data) => {
	        console.log('socket.io => who_is_here');
	        var tokenPayload = JSON.parse(atob(exchangeToken.split('.')[1]));
	        console.log('socket.io <- hello');
	        console.log(tokenPayload.user);
	        socket.emit('hello', tokenPayload.user);
	    });
	    socket.on('ask_image', (data) => {
	        console.log('socket.io => ask_image')
	        new_data = {
	            'sid': data.sid,
	            'image': prepareArtworkToSave()
	        }
	        console.log('socket.io <- full_image');
	        console.log(new_data)
	        socket.emit('full_image', new_data)
	    });
	    socket.on('redirect_full_image', (data) => {
	        console.log('socket.io => redirect_full_image')
	        if (!initComplete) {
	            console.log(data);
	            artwork = data;
	            initialPaintArtwork();
	        }
		});
		socket.on('redirect_changes', (data) => {
			console.log('socket.io => redirect_changes');
			console.log(data);
			var user = data.user;
			var changes = data.changes
			if (changes.cells) {
				var lastCell = null;
				for (var i = 0; i < changes.cells.length; i++) {
					var cell = changes.cells[i];
					paintOnCanvas(cell.col, cell.row, cell.shapeName, cell.color);
					lastCell = cell;
				}
				if (lastCell) {
					drawCollaboratorPointerToCell(data.user, lastCell);
				}
			}
			if (changes.backgroundColor) {
				setBackgroundColor(changes.backgroundColor);
			}
			if (changes.shift) {
				if (changes.shift == 'left') {
					gridArtwork.doShiftLeft(grid);
				} else if (changes.shift == 'right') {
					gridArtwork.doShiftRight(grid);
				} else if (changes.shift == 'up') {
					gridArtwork.doShiftUp(grid);
				} else if (changes.shift == 'down') {
					gridArtwork.doShiftDown(grid);
				}
			}
			if (changes.workspace) {
				applyWorkspaceSize(
					changes.workspace.width, 
					changes.workspace.height, 
					changes.workspace.cellSize, 
					changes.workspace.gridThickness,
					changes.workspace.gridColor,
					changes.workspace.backgroundColor
				);
			}
		});
		socket.on('chat_message', data => {
			console.log('socket.io => chat_message');
			console.log(data);
			showChatMessage(data);
		});
	} else {
	    initialPaintArtwork()
	}
});
