

function GridIsoTriangle_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=isotrianglePath(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(pp, dx, dy))
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridIsoTriangle_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=isotrianglePath(col, row, parent.cellSize);
		var element=paper.path(createSvgTrianglePath(pp, dx, dy))
	    element.attr({"fill": color, "stroke-width":0});
	    return element;
	}   
}

function GridIsoTriangle_ShapeDiamond(parent) {
	this.name="diamond"
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=isotrianglePath(col, row, parent.cellSize);
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

function GridIsoTriangle_ShapeJewel(parent) {
	this.name="diamond"
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		var pp=isotrianglePath(col, row, parent.cellSize);
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



function GridIsoTriangle() {
	this.cellSize=24;
	this.name="iso-triangle";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":"#d0d0d0",
        })
	}
		
	this.paintGrid=function (paper) {
		var colWidth=this.cellSize*sin60;
		var trianglesBehind=Math.floor(paper.width/this.cellSize)
				
		for (var x=0; x<paper.width; x+=2*colWidth) {
			this._createGridLine(paper,["M",x,this.cellSize*sin30,"V",paper.height]);
		}
		
		for (var x=colWidth; x<paper.width; x+=2*colWidth) {
			this._createGridLine(paper,["M",x,0,"V",paper.height]);
		}
		
		for (var y=this.cellSize/2-trianglesBehind*this.cellSize; y<paper.height; y+=this.cellSize) {
			this._createGridLine(paper,["M",0,y,"L",paper.width, y+paper.width*tan30]);
		}
		
		for (var y=this.cellSize/2; y<paper.height+trianglesBehind*this.cellSize; y+=this.cellSize) {
			this._createGridLine(paper,["M",0,y,"L",paper.width,y-paper.width*tan30]);
		}
	}
	
	this.pointToCell=function(x,y) {
		return pointToIsoTriangleCoord(x,y,this.cellSize);
	}
	
	this.getCellRect=function(col, row) {
		var colWidth=this.cellSize*sin60;
		return {
			left: col*colWidth,
			top: row*this.cellSize/2,
			width: colWidth, 
			height: this.cellSize
		}
	}
	
	this.shapes={
		"empty": new GridIsoTriangle_ShapeEmpty(this),
		"flat": new GridIsoTriangle_ShapeFlat(this),
		"diamond": new GridIsoTriangle_ShapeDiamond(this),
		"jewel": new GridIsoTriangle_ShapeJewel(this)
	}
	
	this.shiftLeft={
	    cell_dx:-2,
	    cell_dy:0,
	    dx: -this.cellSize*sin60*2,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:2,
	    cell_dy:0,
	    dx:this.cellSize*sin60*2,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-2,
	    dx: 0,
	    dy: -this.cellSize		
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:2,
	    dx: 0,
	    dy: this.cellSize
	}
}

// Register grid
gridFactory["iso-triangle"]=function() {
	return new GridIsoTriangle();
}

