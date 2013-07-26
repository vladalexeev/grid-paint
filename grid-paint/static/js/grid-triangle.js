

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



function GridTriangle () {
	this.cellSize=24;
	
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
	
	this.getShapeRect=function() {
		return {w:this.cellSize, h:this.cellSize*sin60}
	}
	
	this.shapes={
		"empty": new GridTriangle_ShapeEmpty(this),
		"flat": new GridTriangle_ShapeFlat(this)
	}
	
}
