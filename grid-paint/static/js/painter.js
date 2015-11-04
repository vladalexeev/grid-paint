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

var gridArtwork=new GridArtwork();
var workspaceWidth;
var workspaceHeight;

var undoStack=[];
var redoStack=[];

var selection=new GridSelection();

// 
function adjustCanvasWrapper() {
	$("#canvas-wrapper").height($(window).height()-60);
}

function paintShapeToolButton(shapeName) {
	var shape=grid.shapes[shapeName];
	
	$("#shape-"+shapeName).html("");

	var shapeRect=grid.getCellRect(0,0);
	var shapePaper=new Raphael("shape-"+shapeName, shapeRect.width+20, shapeRect.height+20);
	
	if (shapeName==selectedShapeName) {
		var bgElement=shapePaper.ellipse(shapeRect.width/2+10, shapeRect.height/2+10,
			shapeRect.width/2+10, shapeRect.height/2+10);
		bgElement.attr({"fill":"r#ffffff:40-#cccccc", "stroke-width":0});
	}
	shape.paint(shapePaper, 0, 0, selectedColor, 10, 10);
}

function createShapesToolbar() {
	var shapeElements="";
	for (var shapeName in grid.shapes) {
		shapeElements+='<span id="shape-'+shapeName+
			'" class="grid-shape-button" shape-name="'+
			shapeName+'"></span>';
	}
	
	$("#shapes-toolbar").html(shapeElements);
	
	selectedShapeName="flat";
	for (var shapeName in grid.shapes) {
		paintShapeToolButton(shapeName);
	}
	
	$(".grid-shape-button").click(
		function() {
			selectShape($(this).attr("shape-name"));
		}
	)
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
		var element=grid.shapes[shapeName].paint(paper, col, row, color, 0, 0)
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

function paintOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
			
	if (paperMouseDown) {
		var oldCell=gridArtwork.getCell(cell.col, cell.row)
		var oldShapeName="empty";
		var oldColor="#ffffff";
		if (oldCell) {
			oldShapeName=oldCell.shapeName;
			oldColor=oldCell.color;
		}
		
		newShapeName=selectedShapeName;
		if (event.which==3) {
			newShapeName="empty";
		}
		
		undoStack[undoStack.length-1].pushCellChange(
			cell.col, cell.row, 
			oldShapeName, newShapeName,
			oldColor, selectedColor);
		
		paintOnCanvas(cell.col, cell.row, newShapeName, selectedColor);
		if (newShapeName!="empty") {
			pushRecentColor(selectedColor);	
		}
		changed=true;
	}
}

function selectOnCanvasByMouseEvent(event) {
	var cell=getCellCoordByMouseEvent(event);
	
	if (paperMouseDown) {
		var oldCell=gridArtwork.getCell(cell.col, cell.row)
		
		var cellShapeName="empty";
		var cellColor="#ffffff";
		if (oldCell) {
			cellShapeName=oldCell.shapeName;
			cellColor=oldCell.color;
		}
		
		if (event.which==3) {
			selection.forgetCell(cell.col, cell.row);
		} else {
			var item=selection.saveCell(cell.col, cell.row, cellShapeName, cellColor);
			if (!item.element) {
				item.element=grid.internalShapes["selected"].paint(paper, cell.col, cell.row, "#ffffff", 0, 0); 
			}	
		}
	}
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
	}
}

function setMode(m) {
	mode=m;
	if (mode=="paint") {
		$("#canvas-wrapper").css("cursor","crosshair");
		$("#btn-pick-color").removeAttr("disabled");
		$("#btn-copy-mode").removeAttr("disabled");
		$("#btn-paste-mode").removeAttr("disabled");
	} else if (mode=="pick-color") {
		$("#canvas-wrapper").css("cursor","pointer");
		$("#btn-copy-mode").attr("disabled","disabled");
		$("#btn-paste-mode").attr("disabled","disabled");		
	} else if (mode=="copy") {
		$("#canvas-wrapper").css("cursor","crosshair"); // TODO change cursor
		$("#btn-pick-color").attr("disabled","disabled");
		$("#btn-paste-mode").attr("disabled","disabled");		
	} else if (mode=="paste") {
		$("#canvas-wrapper").css("cursor","crosshair"); // TODO change cursor
		$("#btn-pick-color").attr("disabled","disabled");
		$("#btn-copy-mode").attr("disabled","disabled");
	}
}

function saveArtwork() {
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
			rows:[]	
		}],
		recentColors: recentColors
	}
	
	if (a.effectiveRect.width<0 || a.effectiveRect.height<0) {
		var messageModal=$("#message-modal");
		messageModal.find("#message-text").text("Cannot save empty image");
		messageModal.modal();
		return;
	}
	
	if (artwork.id) {
		a.id=artwork.id;
	}
	
	for (var row=0; row<gridArtwork.cells.length; row++) {
		var rowElement={
			row:row
		}
		var cellArray=[];
		
		for (var col=0; col<gridArtwork.cells[row].length; col++) {
			if (gridArtwork.cells[row][col] && gridArtwork.cells[row][col].shapeName!="empty") {
				cellArray.push([
					col,
					gridArtwork.cells[row][col].shapeName,
					gridArtwork.cells[row][col].color	
				])
			}
		}
		
		rowElement.cells=cellArray;
		a.layers[0].rows.push(rowElement)
	}
	
    $("input[name=artwork_json]").val(JSON.stringify(a));
    changed=false;
    $("form[name=f]")[0].submit();
}

function showPropertiesDialog(modalAction) {
	if (artwork.layers[0].grid=='square') {
		$("#modal_grid_visible_row").show();
	} else {
		$("#modal_grid_visible_row").hide();
	}
	
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

function selectColor(hexColor) {
	selectedColor=hexColor;
	for (var shapeName in grid.shapes) {
		paintShapeToolButton(shapeName);
		$("#selected-color").css("background-color",selectedColor);
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
		for (var i=0; i<undoStep.cellChanges.length; i++) {
			cc=undoStep.cellChanges[i];
			paintOnCanvas(cc.col, cc.row, cc.oldShapeName, cc.oldColor);
		}
		redoStack.push(undoStep);
		updateUndoRedoButtons();
	}
}

function doRedo() {
	if (redoStack.length>0) {
		var redoStep=redoStack.pop();
		for (var i=0; i<redoStep.cellChanges.length; i++) {
			cc=redoStep.cellChanges[i];
			paintOnCanvas(cc.col, cc.row, cc.newShapeName, cc.newColor);
		}
		undoStack.push(redoStep);
		updateUndoRedoButtons();
	}	
}

$(function() {
	adjustCanvasWrapper();
	$(window).resize(
		function() {
			adjustCanvasWrapper();
		})
			
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
	grid.paintGrid(paper);
	createShapesToolbar();
	updateUndoRedoButtons();
	
	$("#toolbar-workspace-width").val(artwork.canvasSize.width);
	$("#toolbar-workspace-height").val(artwork.canvasSize.height);
	$("#toolbar-cell-size").val(artwork.layers[0].cellSize);
	
	
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
	
	$("#canvas")
	.mousedown(
		function(event) {
			paperMouseDown=true;
			updateCellCoordiantesPanel(event);
			
			if (mode=="paint") {
				undoStack.push(new UndoStep());
				redoStack=[];
				updateUndoRedoButtons();
				paintOnCanvasByMouseEvent(event);
			} else if (mode=="pick-color") {
				pickColorByMouseEvent(event);
			} else if (mode=="copy") {
				selectOnCanvasByMouseEvent(event);
			}
		}
	)
	.mouseup(
		function(event) {
			paperMouseDown=false;
		}
	)
	.mousemove(
		function(event) {
			updateCellCoordiantesPanel(event);
			if (mode=="paint") {
				paintOnCanvasByMouseEvent(event);
			} else if (mode=="copy") {
				selectOnCanvasByMouseEvent(event);
			}
		}
	)
	
	$("#color-picker").minicolors({
		inline:true,
		control: "brightness",
		change: function(hex,opacity) {
			selectColor(hex);
		}
	}).minicolors("value",selectedColor);
	
	$("#btn-set-background-color").click(
		function() {
			backgroundColor=selectedColor;
			$("#canvas").css("background-color",backgroundColor);
		}
	)
	
	$("#btn-save").click(
		function() {
			showPropertiesDialog("save");
		}
	)
	
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
			if ($("#modal_artwork_grid_visible")[0].checked) {
				$("#artwork_grid_visible").val('1');
			} else {
				$("#artwork_grid_visible").val('');
			}
			$("#properties-modal").modal('hide');
			
			var modalAction=$("#modal_success_action").val();
			if (modalAction=="save") {
				saveArtwork();
			}
		}
	)
	
	window.onbeforeunload=
		function() {
			if (changed) {
				return "Your drawing was changed. Do you want to leave without saving?";
			}
		}
		
	var tags=$("#modal_artwork_tags");
	tags.tagsinput();
	tags.tagsinput('input').typeahead({
		name: "dataset",
		remote: "/tag-typeahead?query=%QUERY"
    }).bind('typeahead:selected', $.proxy(function (obj, datum) {
      tags.tagsinput('add', datum.value);
      tags.tagsinput('input').typeahead('setQuery', '');
    }, $('input')));
		
	
	//Create color palette
	var paletteHtml="";
	for (var i=0; i<16; i++) {
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
	)
	
	//Fill color palette with recent colors
	if (artwork.recentColors) {
		$paletteDivs=$("#color-palette div");
		for (var i=0; i<$paletteDivs.length && i<artwork.recentColors.length; i++) {
			$($paletteDivs[i]).css("background-color",artwork.recentColors[i]);
			recentColors[i]=artwork.recentColors[i];
		}	
	}
	selectColor(recentColors[0]);
	
	
	$("#btn-pick-color").click(
		function() {
			if (mode=="pick-color") {
			  setMode("paint");
			} else {
			  setMode("pick-color");
			}
		}
	);
	
	setMode("paint");
	
	$("#btn-shift-left").click(
		function() {
			gridArtwork.doShiftLeft(grid);
			changed=true;
		});
	
	$("#btn-shift-right").click(
		function() {
			gridArtwork.doShiftRight(grid);
			changed=true;
		});
		
	$("#btn-shift-up").click(
		function() {
			gridArtwork.doShiftUp(grid);
			changed=true;
		});
		
	$("#btn-shift-down").click(
		function() {
			gridArtwork.doShiftDown(grid);
			changed=true;
		});
		
	$("#btn-undo").click(
		function() {
			doUndo();
		});
		
	$("#btn-redo").click(
		function() {
			doRedo();
		});
		
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
			}
		});
		
	$("#btn-apply-workspace-size").click(
		function() {
			var newWidth=parseInt($("#toolbar-workspace-width").val(),10);
			var newHeight=parseInt($("#toolbar-workspace-height").val(),10);
			var newCellSize=parseInt($("#toolbar-cell-size").val(),10);
			
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
			
			$("#canvas")
				.css("width",newWidth)
				.css("height",newHeight);
			grid.workspaceWidth=newWidth;
			grid.workspaceHeight=newHeight;
			grid.cellSize=newCellSize;
			
			paper.remove();
			paper=new Raphael("canvas",newWidth,newHeight);
			grid.paintGrid(paper);
			createShapesToolbar();
			
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
		
	$("#btn-copy-mode").click(
		function(event) {
			if (mode=="paint") {
				setMode("copy");
				selection=new GridSelection();
			} else if (mode=="copy") {
				selection.hideSelection();
				setMode("paint");
			}
		});
	
	$("#btn-paste-mode").click(
		function(event) {
			if (mode=="paint") {
				setMode("paste");
			} else if (mode=="paste") {
				setMode("paint");
			}
		});
	
})
