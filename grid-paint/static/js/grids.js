var sin30=Math.sin(Math.PI/6);
var sin60=Math.sin(60/180*Math.PI);
var cos30=Math.cos(30/180*Math.PI);
var cos60=Math.cos(60/180*Math.PI);
var tan30=Math.tan(30/180*Math.PI);
var tan60=Math.tan(60/180*Math.PI);

var gridLineColor="#d0d0d0";

var gridFactory=[];

function hexToHsl(hex) {
	return Raphael.color(hex);
}

function hslToHex(h,s,l) {
	if (h<0) {
		h=0;
	}
	if (h>1) {
		h=1;
	}
	if (s<0) {
		s=0;
	}
	if (s>1) {
		s=1;
	}
	if (l<0) {
		l=0;
	}
	if (l>1) {
		l=1;
	}
	
	return Raphael.hsl(h,s,l);
}

/*
 * Convert string ing format 'rgb(25,30,165)' to hex color string
 */
function rgb2hex(rgb) {
     if (  rgb.search("rgb") == -1 ) {
          return rgb;
     }
     else if ( rgb == 'rgba(0, 0, 0, 0)' ) {
         return 'transparent';
     }
     else {
          rgb = rgb.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+))?\)$/);
          function hex(x) {
               return ("0" + parseInt(x).toString(16)).slice(-2);
          }
          return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]); 
     }
}


function GridArtwork() {
    this.cells=[];
    
    // Set item cell to the artwork
    // The function returns artwork item
    // Example {shapeName:"flat", color:"#ff0000", element:[Object]}
    this.setCell=function (col, row, shapeName, color) {
        while (this.cells.length<=row) {
            this.cells[this.cells.length]=[];
        }

        while (this.cells[row].length<=col) {
            this.cells[row][this.cells[row].length]=null;
        }
        
        var oldCell=this.cells[row][col];
        
        
        if (oldCell && oldCell.shapeName==shapeName && oldCell.color==color) {
            return oldCell;
        } else {
        	if (oldCell && oldCell.element) {
        		oldCell.element.remove();
        	}
        	
            this.cells[row][col]= {
                shapeName: shapeName,
                color: color
            };
            return this.cells[row][col];
        }        
    };
    
    this.getCell=function(col, row) {
        if (this.cells.length<=row) {
            return null;
        }
        
        if (this.cells[row].length<=col) {
            return null;
        }
        
        return this.cells[row][col];
    };
    
    this._shiftAllElements=function(dx, dy) {
    	for (var row=0; row<this.cells.length; row++) {
 			for (var col=0; col<this.cells[row].length; col++) {
 				if (this.cells[row][col]) {
 					if (this.cells[row][col].element) {
 						this.cells[row][col].element.translate(dx, dy);
 					} 
 				}
 			}
 		}
    };
    
    this.doShiftLeft=function(grid) {
        var shift=grid.shiftLeft;
        for (var row=0; row<this.cells.length; row++) {
            for (var col=0; col<Math.min(-shift.cell_dx, this.cells[row].length); col++) {
                if (this.cells[row][col]) {
                    this.cells[row][col].element.remove();
                }
            }
            
            this.cells[row]=this.cells[row].slice(-shift.cell_dx);
        }
        
        this._shiftAllElements(shift.dx, shift.dy);
    };
    
    this.doShiftRight=function(grid) {
    	var shift=grid.shiftRight;
    	for (var row=0; row<this.cells.length; row++) {
    		for (var i=0; i<shift.cell_dx; i++) {
    			this.cells[row].unshift(null);
    		}
    	}
    	
    	this._shiftAllElements(shift.dx, shift.dy);
 	};
 	
 	this.doShiftUp=function(grid) {
 		var shift=grid.shiftUp;
 		for (var row=0; row<-shift.cell_dy; row++) {
 			for (var col=0; col<this.cells[row].length; col++) {
 				if (this.cells[row][col]) {
 					this.cells[row][col].element.remove();
 				}
 			}
 		}
 		
 		this.cells=this.cells.slice(-shift.cell_dy);

		this._shiftAllElements(shift.dx, shift.dy);
 	};
 	
 	this.doShiftDown=function(grid) {
 		var shift=grid.shiftDown;
 		for (var row=0; row<shift.cell_dy; row++) {
 			this.cells.unshift([]);
 		}

		this._shiftAllElements(shift.dx, shift.dy); 		
 	};
}

/*
 * Interface of Grid
 *   function paintGrid(paper) - paints grid on a paper 
 * 
 *   function pointToCell(x,y) - convert mouse coordinates to cell indices.
 *     example of returning object: {col:10, row:15}
 * 
 *   function getCellRect(col, row) - bounding rectangle {left:24, top:24, width: 24, height:24}
 *  
 * 
 *  Interface of Shape
 *   function paint(paper, point{x,y}, color)
 */


/**
 * convert mouse coordinate to triangle grid coordinate.
 * Uses in 'triangle' and 'hex' grids 
 */
function pointToTriangleCoord(x,y,sideLength) {
	var rowHeight=sideLength*sin60;
	var cellY=Math.floor(y/rowHeight);
	    
    var relativeY;
    if (cellY % 2 == 0) {
        relativeY=y-cellY*rowHeight;
    } else {
        relativeY=y-(cellY-1)*rowHeight;
    }
	    	    
    var A1=-tan60;
    var B1=-1;
    var C1=-sideLength*sin60;
    var dist1=Math.abs(A1*x+B1*relativeY+C1)/Math.sqrt(A1*A1+B1*B1);
    var d1=Math.floor(dist1/rowHeight)-1;
	    
    var A2=-tan60;
    var B2=1;
    var C2=-3*sideLength*sin60;
    var dist2=Math.abs(A2*x+B2*relativeY+C2)/Math.sqrt(A2*A2+B2*B2);
    var d2=Math.floor(dist2/rowHeight)-1;
        
    return {col:d1+d2, row:cellY};
}

/**
 * Convert mouse coordiante to iso-triangle grid coordinate.
 * Used in 'iso-triangle' and 'iso-hex' grids
 */
function pointToIsoTriangleCoord(x,y,sideLength) {
	var colWidth=sideLength*sin60;
	var cellX=Math.floor(x/colWidth);
	    
    var relativeX;
    if (cellX % 2 == 0) {
        relativeX=x-cellX*colWidth;
    } else {
        relativeX=x-(cellX-1)*colWidth;
    }
	    	    
    var A1=-tan60;
    var B1=-1;
    var C1=-sideLength*sin60;
    var dist1=Math.abs(A1*y+B1*relativeX+C1)/Math.sqrt(A1*A1+B1*B1);
    var d1=Math.floor(dist1/colWidth)-1;
	    
    var A2=-tan60;
    var B2=1;
    var C2=-3*sideLength*sin60;
    var dist2=Math.abs(A2*y+B2*relativeX+C2)/Math.sqrt(A2*A2+B2*B2);
    var d2=Math.floor(dist2/colWidth)-1;
        
    return {col:cellX, row:d1+d2};
}

/**
 * get path and center point of triangle by it's cell coordinates.
 * Used in 'triangle' and 'hex' grids
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 * @return array of four points: points [0,1,2] - corners, point[3] - center point
 */
function trianglePath(col, row, sideLength) {
	rowHeight=sideLength*sin60;
	x=col*sideLength/2;
	y=row*rowHeight;
	if (row % 2 == 0) {
		if (col % 2 == 0) {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				];
		} else {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				];
		}
	} else {
		if (col % 2 == 0) {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				];
		} else {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				];
		}
	}
}


/**
 * Get path and center point of isometric triangle by it's cell coordinates.
 * Used in 'iso-triangle' and 'iso-hex' grids
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 * @return array of four points: points [0,1,2] - corners, point[3] - center point
 */
function isotrianglePath(col, row, sideLength) {
	colWidth=sideLength*sin60;
	y=row*sideLength/2;;
	x=col*colWidth;
	if (col % 2 == 0) {
		if (row % 2 == 0) {
			return [
				{y:y, x:x+colWidth},
				{y:y+sideLength/2, x:x},
				{y:y+sideLength, x:x+colWidth},
				{y:y+sideLength/2, x:x+colWidth*2/3}
				];
		} else {
			return [
				{y:y, x:x},
				{y:y+sideLength, x:x},
				{y:y+sideLength/2, x:x+colWidth},
				{y:y+sideLength/2, x:x+colWidth/3}
				];
		}
	} else {
		if (row % 2 == 0) {
			return [
				{y:y, x:x},
				{y:y+sideLength, x:x},
				{y:y+sideLength/2, x:x+colWidth},
				{y:y+sideLength/2, x:x+colWidth/3}
				];
		} else {
			return [
				{y:y, x:x+colWidth},
				{y:y+sideLength/2, x:x},
				{y:y+sideLength, x:x+colWidth},
				{y:y+sideLength/2, x:x+colWidth*2/3}
				];
		}
	}
}


function UndoStep() {
	this.cellChanges=[];
	
	this.pushCellChange=function(col, row, oldShapeName, newShapeName, oldColor, newColor) {
		for (var i=0; i<this.cellChanges.length; i++) {
			var cc=this.cellChanges[i];
			if (cc.col==col && cc.row==row) {
				return;
			}
		}
		
		this.cellChanges.push({
			col: col,
			row: row,
			oldShapeName: oldShapeName, 
			newShapeName: newShapeName,
			oldColor: oldColor,
			newColor: newColor
		});
	};
	
	this.setBackgroundChange=function(oldColor, newColor) {
		this.backgroundChange= {
			oldColor: oldColor,
			newColor: newColor
		};
	};
	
	this.setShiftChange=function(shiftCol, shiftRow, cells) {
		this.shiftChange({
			shiftCol: shiftCol,
			shiftRow: shiftRow,
			cells: cells
		});
	};
}

function GridSelection() {
	this.cells=[];
	this.grid=null;
	this.paper=null;
	
	this.saveCell=function(col, row, shapeName, color) {
		for (var i=0; i<this.cells.length; i++) {
			var cc=this.cells[i];
			if (cc.col==col && cc.row==row) {
				return cc;
			}
		}
		
		var element=this.grid.internalShapes["selected"].paint(this.paper, col, row, "#ffffff", 0, 0);
		
		var item={
			col: col,
			row: row,
			shapeName: shapeName,
			color: color,
			element: element
		};
		
		this.cells.push(item);
		return item;
	};
	
	this.forgetCell=function(col, row) {
		var index=-1;
		for (var i=0; i<this.cells.length; i++) {
			var cc=this.cells[i];
			if (cc.col==col && cc.row==row) {
				index=i;
				break;
			}
		}
		
		if (index>=0) {
			if (this.cells[index].element) {
				this.cells[index].element.remove();
			}
			
			this.cells.splice(index,1);
		}
	};
	
	this.isEmpty=function() {
		return this.cells.length==0;
	};
	
	this._deleteElements=function() {
		for (var i=0; i<this.cells.length; i++) {
			var cc=this.cells[i];
			if (cc.element) {
				cc.element.remove();
				delete cc.element;
			}
		}		
	};
	
	this.copyPrepare=function() {
		this.cells=[];
	};
	
	this.copyFinished=function() {
		this._deleteElements();
		
		//Calculate base cell
		var minCol=10000;
		var minRow=10000;
		for (var i=0; i<this.cells.length; i++) {
			var cc=this.cells[i];
			if (cc.col<minCol) {
				minCol=cc.col;
			}
			
			if (cc.row<minRow) {
				minRow=cc.row;
			}
		}
		
		this.baseCol=minCol;
		this.baseRow=minRow;
		
		//Save selection to LocalStorage
		var arr=[];
		for (var i=0; i<this.cells.length; i++) {
			var c=this.cells[i];
			arr.push(
				[c.col, c.row, c.shapeName, c.color]);
		}

		localStorage['gridSelectionType']=this.grid.name;		
		localStorage['gridSelection']=JSON.stringify({
			selection: arr,
			base: {
				col: this.baseCol,
				row: this.baseRow
			}
		});
	};
	
	this.loadFromLocalStorage=function() {
		if (this.grid.name==localStorage['gridSelectionType']) {
			var s=JSON.parse(localStorage['gridSelection']);
			for (var i=0; i<s.selection.length; i++) {
				var ss=s.selection[i];
				this.cells.push({
					col: ss[0],
					row: ss[1],
					shapeName: ss[2],
					color: ss[3]
				});
			}
			
			this.baseCol=s.base.col;
			this.baseRow=s.base.row;
		}
	};
	
	this.pastePrepare=function() {
		for (var i=0; i<this.cells.length; i++) {
			var cc=this.cells[i];
			cc.element=this.grid.internalShapes["selected"].paint(this.paper, cc.col, cc.row, "#ffffff", 0, 0);
		}
		
		this.pasteCol=this.baseCol;
		this.pasteRow=this.baseRow;
	};
	
	this.pasteFinished=function() {
		this._deleteElements();
	};
	
	this.changePasteCell=function(col, row) {
		var oldCellRect=this.grid.getCellRect(this.pasteCol, this.pasteRow);
		var newCellRect=this.grid.getCellRect(col, row);
		var dx=newCellRect.left-oldCellRect.left;
		var dy=newCellRect.top-oldCellRect.top;
		
		for (var i=0; i<this.cells.length; i++) {
			this.cells[i].element.translate(dx,dy);
		}
		this.pasteCol=col;
		this.pasteRow=row;
	};
}

