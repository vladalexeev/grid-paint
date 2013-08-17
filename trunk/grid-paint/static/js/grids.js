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
            }
            return this.cells[row][col];
        }        
    }
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



function pointToTriangleCoord(x,y,sideLength) {
	var rowHeight=sideLength*sin60;
	var cellY=Math.floor(y/rowHeight);
	    
    var relativeY;
    if (cellY % 2 == 0) {
        relativeY=y-cellY*rowHeight;
    } else {
        relativeY=y-(cellY-1)*rowHeight
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
        
    return {col:d1+d2, row:cellY}
}

/**
 * get path and center point of triangle by it's cell coordinates 
 * @param {Object} col
 * @param {Object} row
 * @param {Object} sideLength
 * @return array of four points: points [0,1,2] - corners, point[3] - center point
 */
function trianglePath(col, row, sideLength) {
	rowHeight=sideLength*sin60
	x=col*sideLength/2
	y=row*rowHeight;
	if (row % 2 == 0) {
		if (col % 2 == 0) {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				]
		} else {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				]
		}
	} else {
		if (col % 2 == 0) {
			return [
				{x:x, y:y},
				{x:x+sideLength, y:y},
				{x:x+sideLength/2, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight/3}
				]
		} else {
			return [
				{x:x, y:y+rowHeight},
				{x:x+sideLength/2, y:y},
				{x:x+sideLength, y:y+rowHeight},
				{x:x+sideLength/2, y:y+rowHeight*2/3}
				]
		}
	}
}


