

function createSvgTrianglePath(pathPoints, dx, dy) {
	return [
		"M", pathPoints[0].x+dx, pathPoints[0].y+dy,
		"L", pathPoints[1].x+dx, pathPoints[1].y+dy,
		"L", pathPoints[2].x+dx, pathPoints[2].y+dy, "Z"
	]
}

function GridTriangle_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=trianglePath(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(pp, dx, dy))
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridTriangle_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=trianglePath(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(pp, dx, dy))
	    element.attr({"fill": color, "stroke-width":0});
	    return element;
	}   
}

function GridTriangle_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=trianglePath(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(pp, dx, dy))
	    element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0});
	    return element;
	}
}

function GridTriangle_ShapeDiamond(parent) {
	this.name="diamond"
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=trianglePath(col, row, parent.cellSize);
		var c=hexToHsl(color);
		paper.setStart();
		
        var c1=hslToHex(c.h, c.s, c.l+0.2);
        var e1=paper.path([
        	"M", pp[0].x+dx, pp[0].y+dy,
        	"L", pp[1].x+dx, pp[1].y+dy,
        	"L", pp[3].x+dx, pp[3].y+dy,"Z"
        ])
        e1.attr({"fill":c1, "stroke-width":0})
        
        var c2=hslToHex(c.h, c.s, c.l+0.1);
        var e2=paper.path([
        	"M", pp[0].x+dx, pp[0].y+dy,
        	"L", pp[2].x+dx, pp[2].y+dy,
        	"L", pp[3].x+dx, pp[3].y+dy,"Z"
        ])
        e2.attr({"fill":c2, "stroke-width":0})
        
        var c3=hslToHex(c.h, c.s, c.l-0.1);
        var e3=paper.path([
        	"M", pp[1].x+dx, pp[1].y+dy,
        	"L", pp[2].x+dx, pp[2].y+dy,
        	"L", pp[3].x+dx, pp[3].y+dy,"Z"
        ])
        e3.attr({"fill":c3, "stroke-width":0})
        
        return paper.setFinish();
	}
}

function GridTriangle_ShapeJewel(parent) {
	this.name="diamond"
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=trianglePath(col, row, parent.cellSize);
		var c=hexToHsl(color);
		paper.setStart();
		
        var c1=hslToHex(c.h, c.s, c.l+0.2);
        var e1=paper.path([
        	"M", pp[0].x+dx, pp[0].y+dy,
        	"L", pp[1].x+dx, pp[1].y+dy,
        	"L", pp[1].x+(pp[3].x-pp[1].x)/2+dx, pp[1].y+(pp[3].y-pp[1].y)/2+dy,
        	"L", pp[0].x+(pp[3].x-pp[0].x)/2+dx, pp[0].y+(pp[3].y-pp[0].y)/2+dy,
        	"Z"
        ])
        e1.attr({"fill":c1, "stroke-width":0})
        
        var c2=hslToHex(c.h, c.s, c.l+0.1);
        var e2=paper.path([
        	"M", pp[0].x+dx, pp[0].y+dy,
        	"L", pp[2].x+dx, pp[2].y+dy,
        	"L", pp[2].x+(pp[3].x-pp[2].x)/2+dx, pp[2].y+(pp[3].y-pp[2].y)/2+dy,
        	"L", pp[0].x+(pp[3].x-pp[0].x)/2+dx, pp[0].y+(pp[3].y-pp[0].y)/2+dy,
        	"Z"
        ])
        e2.attr({"fill":c2, "stroke-width":0})
        
        var c3=hslToHex(c.h, c.s, c.l-0.1);
        var e3=paper.path([
        	"M", pp[1].x+dx, pp[1].y+dy,
        	"L", pp[2].x+dx, pp[2].y+dy,
        	"L", pp[2].x+(pp[3].x-pp[2].x)/2+dx, pp[2].y+(pp[3].y-pp[2].y)/2+dy,
        	"L", pp[1].x+(pp[3].x-pp[1].x)/2+dx, pp[1].y+(pp[3].y-pp[1].y)/2+dy,
        	"Z"
        ])
        e3.attr({"fill":c3, "stroke-width":0})
        
        var e4=paper.path([
        	"M", pp[0].x+(pp[3].x-pp[0].x)/2+dx, pp[0].y+(pp[3].y-pp[0].y)/2+dy,
        	"L", pp[1].x+(pp[3].x-pp[1].x)/2+dx, pp[1].y+(pp[3].y-pp[1].y)/2+dy,
        	"L", pp[2].x+(pp[3].x-pp[2].x)/2+dx, pp[2].y+(pp[3].y-pp[2].y)/2+dy,
        	"Z"
        ])
        e4.attr({"fill":color, "stroke-width":0})
        
        return paper.setFinish();
	}	
}



function GridTriangle () {
	this.cellSize=24;
	this.name="triangle";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
	}
		
	this.paintGrid=function (paper) {
		var rowHeight=this.cellSize*sin60;
		var trianglesBehind=Math.floor(paper.height/this.cellSize)
				
		for (var y=0; y<paper.height; y+=2*rowHeight) {
			this._createGridLine(paper,["M",this.cellSize*sin30,y,"H",paper.width]);
		}
		
		for (var y=rowHeight; y<paper.height; y+=2*rowHeight) {
			this._createGridLine(paper,["M",0,y,"H",paper.width]);
		}
		
		for (var x=this.cellSize/2-trianglesBehind*this.cellSize; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x+paper.height*tan30,paper.height]);
		}
		
		for (var x=this.cellSize/2; x<paper.width+trianglesBehind*this.cellSize; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x-paper.height*tan30,paper.height]);
		}
	}
	
	this.pointToCell=function(x,y) {
		return pointToTriangleCoord(x,y,this.cellSize);
	}
	
	this.getCellRect=function(col, row) {
		var rowHeight=this.cellSize*sin60;
		return {
			left: col*this.cellSize/2,
			top: row*rowHeight,
			width: this.cellSize,
			height: rowHeight
		}
	}
	
	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		var sum1=col+row;
		var sum2=nearCol+nearRow;
		
		if ((sum1 % 2)!=(sum2 % 2)) {
			return {
				col: nearCol,
				row: nearRow+1
			}
		} else {
			return {
				col: nearCol,
				row: nearRow
			}
		}
	}
	
	this.shapes={
		"empty": new GridTriangle_ShapeEmpty(this),
		"flat": new GridTriangle_ShapeFlat(this),
		"diamond": new GridTriangle_ShapeDiamond(this),
		"jewel": new GridTriangle_ShapeJewel(this)
	}
	
	this.internalShapes={
	    "selected": new GridTriangle_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-2,
	    cell_dy:0,
	    dx: -this.cellSize,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:2,
	    cell_dy:0,
	    dx: this.cellSize,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-2,
	    dx: 0,
	    dy: -this.cellSize*sin60*2
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:2,
	    dx:0,
	    dy: this.cellSize*sin60*2
	}

}

// Register grid
gridFactory["triangle"]=function() {
	return new GridTriangle();
}

