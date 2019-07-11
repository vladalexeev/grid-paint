/*
 * Square grid
 */

function GridSquare_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
	    var element=paper.rect(x,y,this.parent.cellSize,this.parent.cellSize);
	    element.attr({"stroke":"#808080"});
	    return element;
	};   
}

function GridSquare_BasicShapeFlat(parent) {
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var cellSize=this.parent.cellSize;
        var facet=this.getFacet();		
		var element=paper.rect(
			x+facet,
			y+facet,
			cellSize-facet*2,
			cellSize-facet*2);
		element.attr({"fill":color, "stroke-width":0});
		return element;
	};
}

function GridSquare_ShapeFlat(parent) {
	this.super=GridSquare_BasicShapeFlat;
	this.super(parent);
	this.name='flat';
	this.getFacet=function() {
		return 0;
	};
}

function GridSquare_ShapeFlat1(parent) {
	this.super=GridSquare_BasicShapeFlat;
	this.super(parent);
	
	this.name="flat1";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	};
}

function GridSquare_ShapeFlat2(parent) {
    this.super=GridSquare_BasicShapeFlat;
    this.super(parent);
    
    this.name="flat2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    };
}

function GridSquare_ShapeFlat3(parent) {
    this.super=GridSquare_BasicShapeFlat;
    this.super(parent);
    
    this.name="flat3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    };
}

function GridSquare_BasicShapeCircle(parent) {
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var cellSize=this.parent.cellSize;
        var facet=this.getFacet();		
		var element=paper.circle(
			x+cellSize/2,
			y+cellSize/2,
			cellSize/2-facet);
		element.attr({"fill":color, "stroke-width":0});
		return element;
	};
}

function GridSquare_ShapeCircle(parent) {
	this.super=GridSquare_BasicShapeCircle;
	this.super(parent);
	this.name='circle';
	this.getFacet=function() {
		return 0;
	};
}

function GridSquare_ShapeCircle1(parent) {
	this.super=GridSquare_BasicShapeCircle;
	this.super(parent);
	
	this.name="circle1";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	};
}

function GridSquare_ShapeCircle2(parent) {
    this.super=GridSquare_BasicShapeCircle;
    this.super(parent);
    
    this.name="circle2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    };
}

function GridSquare_ShapeCircle3(parent) {
    this.super=GridSquare_BasicShapeCircle;
    this.super(parent);
    
    this.name="circle3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    };
}


function GridSquare_ShapeSelected(parent) {
	this.name="selected";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;		
		var element=paper.rect(x,y,this.parent.cellSize,this.parent.cellSize);
		element.attr({
			"fill":"url('/img/selection-hatch.png')", 
			"fill-opacity": 0.5,
			"stroke-width":0})
		return element;
	}	
}

function GridSquare_ShapeDiamond(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;
		var c=hexToHsl(color);
		cellSize=this.parent.cellSize;
				
		paper.setStart();
				
		var c1=hslToHex(c.h, c.s, c.l+0.2);
		var e1=paper.path([
			"M ",x, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y,"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2=hslToHex(c.h, c.s, c.l+0.1);
		var e2=paper.path([
			"M",x, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x, y+cellSize,"Z"])
		e2.attr({"fill":c2, "stroke-width":0});
				
		var c3=hslToHex(c.h, c.s, c.l-0.1);
		var e3=paper.path([
			"M",x, y+cellSize,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y+cellSize,"Z"]);
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4=hslToHex(c.h, c.s, c.l-0.2);
		var e4=paper.path([
			"M",x+cellSize, y,
			"L",x+cellSize/2, y+cellSize/2,
			"L",x+cellSize, y+cellSize,"Z"]);
		e4.attr({"fill":c4, "stroke-width":0});
		return paper.setFinish();
	}			
}

function GridSquare_BasicShapeJewel(parent) {
    this.parent=parent;
    this.paint=function(paper, col, row, color, dx, dy) {
		x=col*parent.cellSize+dx;
		y=row*parent.cellSize+dy;    	
        var c=hexToHsl(color);
        var cellSize=this.parent.cellSize;
        var facet=this.getFacet();
                
        paper.setStart();
        var c1=hslToHex(c.h, c.s, c.l+0.2);
        var e1=paper.path([
            "M ",x, y,
            "L",x+facet, y+facet,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize, y,"Z"]);
        e1.attr({"fill":c1, "stroke-width":0});
                
        var c2=hslToHex(c.h, c.s, c.l+0.1);
        var e2=paper.path([
            "M",x, y,
            "L",x+facet, y+facet,
            "L",x+facet, y+cellSize-facet,
            "L",x, y+cellSize,"Z"])
        e2.attr({"fill":c2, "stroke-width":0});
                
        var c3=hslToHex(c.h, c.s, c.l-0.1);
        var e3=paper.path([
            "M",x, y+cellSize,
            "L",x+facet, y+cellSize-facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+cellSize, y+cellSize,"Z"]);
        e3.attr({"fill":c3, "stroke-width":0});
                
        var c4=hslToHex(c.h, c.s, c.l-0.2);
        var e4=paper.path([
            "M",x+cellSize, y,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+cellSize, y+cellSize,"Z"]);
        e4.attr({"fill":c4, "stroke-width":0});
                
        var e5=paper.path([
            "M",x+facet, y+facet,
            "L",x+cellSize-facet, y+facet,
            "L",x+cellSize-facet, y+cellSize-facet,
            "L",x+facet, y+cellSize-facet,"Z"]);
        e5.attr({"fill":color, "stroke-width":0});
        return paper.setFinish();
    }    
}

function GridSquare_ShapeJewel(parent) {
	this.super=GridSquare_BasicShapeJewel;
	this.super(parent);
	
	this.name="jewel";
	this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/6;	    
	}
}

function GridSquare_ShapeJewel2(parent) {
    this.super=GridSquare_BasicShapeJewel;
    this.super(parent);
    
    this.name="jewel2";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/4;      
    }
}

function GridSquare_ShapeJewel3(parent) {
    this.super=GridSquare_BasicShapeJewel;
    this.super(parent);
    
    this.name="jewel3";
    this.getFacet=function() {
        var cellSize=this.parent.cellSize;
        return cellSize/3;      
    }
}

function GridSquare() {
	this.cellSize=24;
	this.name="square";
	
	this._createGridLine=function(paper, pathArray) {
		var path=paper.path(pathArray);
        path.attr({
            "stroke":gridLineColor,
        })
	}
	
	this.paintGrid=function (paper) {
		for (var y=0; y<paper.height; y+=this.cellSize) {
			this._createGridLine(paper,["M",0,y,"L",paper.width,y]);
		}
		
		for (var x=0; x<paper.width; x+=this.cellSize) {
			this._createGridLine(paper,["M",x,0,"L",x,paper.height]);
		}			
	}
	
	this.pointToCell=function(x,y) {
        var cellX=Math.floor(x/this.cellSize);
        var cellY=Math.floor(y/this.cellSize);	    
        return {col: cellX, row: cellY};
	}
	
	this.getCellRect=function(col, row) {
	    return {
	        left: col*this.cellSize,
	        top: row*this.cellSize,
	        width: this.cellSize,
	        height: this.cellSize
	    }
	}
	
	this.nearestSameCell=function(col, row, nearCol, nearRow) {
		return {
			col: nearCol,
			row: nearRow
		};
	}
	
	this.getAdjacentCells = function(col, row) {
		return [
			{
				col: col - 1,
				row: row
			},
			{
				col: col,
				row: row - 1
			},
			{
				col: col + 1,
				row: row
			},
			{
				col: col,
				row: row + 1
			}
		]
	}
	
	this.isCellInsideWorkspace = function(col, row) {
		var colCount=this.workspaceWidth/this.cellSize;
		var rowCount=this.workspaceHeight/this.cellSize;
		return col>=0 && col<colCount && row>=0 && row<rowCount;
	}
	
	this.shapes={
	    "empty": new GridSquare_ShapeEmpty(this),
		"flat": new GridSquare_ShapeFlat(this),
		"flat1": new GridSquare_ShapeFlat1(this),
		"flat2": new GridSquare_ShapeFlat2(this),
		"flat3": new GridSquare_ShapeFlat3(this),
		'circle': new GridSquare_ShapeCircle(this),
		'circle1': new GridSquare_ShapeCircle1(this),
		'circle2': new GridSquare_ShapeCircle2(this),
		'circle3': new GridSquare_ShapeCircle3(this),
		"jewel": new GridSquare_ShapeJewel(this),
		"jewel2": new GridSquare_ShapeJewel2(this),
		"jewel3": new GridSquare_ShapeJewel3(this),
		"diamond": new GridSquare_ShapeDiamond(this),
	};
	
	this.internalShapes={
	    "selected": new GridSquare_ShapeSelected(this)
	}
	
	this.shiftLeft={
	    cell_dx:-1,
	    cell_dy:0,
	    dx: -this.cellSize,
	    dy: 0
	}
	
	this.shiftRight={
	    cell_dx:1,
	    cell_dy:0,
	    dx: this.cellSize,
	    dy: 0
	}
	
	this.shiftUp={
	    cell_dx:0,
	    cell_dy:-1,
	    dx: 0,
	    dy: -this.cellSize
	}
	
	this.shiftDown={
	    cell_dx:0,
	    cell_dy:1,
	    dx:0,
	    dy: this.cellSize
	}
}

// Register grid
gridFactory["square"]=function() {
	return new GridSquare();
}

