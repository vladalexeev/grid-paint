/*
 * Square grid
 */

function GridSquare_ShapeEmpty(parent) {
	this.name="empty";
	this.parent=parent;
	this.paint=function(paper, point, color) {
	    var element=paper.rect(point.x,point.y,this.parent.cellSize,this.parent.cellSize);
	    element.attr({"stroke":"#808080"});
	    return element;
	}   
}

function GridSquare_ShapeFlat(parent) {
	this.name="flat";
	this.parent=parent;
	this.paint=function(paper, point, color) {
		var element=paper.rect(point.x,point.y,this.parent.cellSize,this.parent.cellSize);
		element.attr({"fill":color, "stroke-width":0})
		return element;
	}
}

function GridSquare_ShapeDiamond(parent) {
	this.name="diamond";
	this.parent=parent;
	this.paint=function(paper, point, color) {
		var c=hexToHsl(color);
		cellSize=this.parent.cellSize;
				
		paper.setStart();
				
		var c1=hslToHex(c.h, c.s, c.l+0.2);
		var e1=paper.path([
			"M ",point.x, point.y,
			"L",point.x+cellSize/2, point.y+cellSize/2,
			"L",point.x+cellSize, point.y,"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2=hslToHex(c.h, c.s, c.l+0.1);
		var e2=paper.path([
			"M",point.x, point.y,
			"L",point.x+cellSize/2, point.y+cellSize/2,
			"L",point.x, point.y+cellSize,"Z"])
		e2.attr({"fill":c2, "stroke-width":0});
				
		var c3=hslToHex(c.h, c.s, c.l-0.1);
		var e3=paper.path([
			"M",point.x, point.y+cellSize,
			"L",point.x+cellSize/2, point.y+cellSize/2,
			"L",point.x+cellSize, point.y+cellSize,"Z"]);
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4=hslToHex(c.h, c.s, c.l-0.2);
		var e4=paper.path([
			"M",point.x+cellSize, point.y,
			"L",point.x+cellSize/2, point.y+cellSize/2,
			"L",point.x+cellSize, point.y+cellSize,"Z"]);
		e4.attr({"fill":c4, "stroke-width":0});
		return paper.setFinish();
	}			
}

function GridSquare_ShapeJewel(parent) {
	this.name="jewel";
	this.parent=parent;
	this.paint=function(paper, point, color) {
		var c=hexToHsl(color);
		var cellSize=this.parent.cellSize;
		var facet=cellSize/6;
				
		paper.setStart();
		var c1=hslToHex(c.h, c.s, c.l+0.2);
		var e1=paper.path([
			"M ",point.x, point.y,
			"L",point.x+facet, point.y+facet,
			"L",point.x+cellSize-facet, point.y+facet,
			"L",point.x+cellSize, point.y,"Z"]);
		e1.attr({"fill":c1, "stroke-width":0});
				
		var c2=hslToHex(c.h, c.s, c.l+0.1);
		var e2=paper.path([
			"M",point.x, point.y,
			"L",point.x+facet, point.y+facet,
			"L",point.x+facet, point.y+cellSize-facet,
			"L",point.x, point.y+cellSize,"Z"])
				e2.attr({"fill":c2, "stroke-width":0});
				
		var c3=hslToHex(c.h, c.s, c.l-0.1);
		var e3=paper.path([
			"M",point.x, point.y+cellSize,
			"L",point.x+facet, point.y+cellSize-facet,
			"L",point.x+cellSize-facet, point.y+cellSize-facet,
			"L",point.x+cellSize, point.y+cellSize,"Z"]);
		e3.attr({"fill":c3, "stroke-width":0});
				
		var c4=hslToHex(c.h, c.s, c.l-0.2);
		var e4=paper.path([
			"M",point.x+cellSize, point.y,
			"L",point.x+cellSize-facet, point.y+facet,
			"L",point.x+cellSize-facet, point.y+cellSize-facet,
			"L",point.x+cellSize, point.y+cellSize,"Z"]);
		e4.attr({"fill":c4, "stroke-width":0});
				
		var e5=paper.path([
			"M",point.x+facet, point.y+facet,
			"L",point.x+cellSize-facet, point.y+facet,
			"L",point.x+cellSize-facet, point.y+cellSize-facet,
			"L",point.x+facet, point.y+cellSize-facet,"Z"]);
				e5.attr({"fill":color, "stroke-width":0});
		return paper.setFinish();
	}

}

function GridSquare() {
	this.cellSize=24;
	
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
	
	this.getShapeRect=function() {
		return {w:this.cellSize, h:this.cellSize};
	}
	
	this.pointToCell=function(x,y) {
        var cellX=Math.floor(x/this.cellSize);
        var cellY=Math.floor(y/this.cellSize);	    
        return {col: cellX, row: cellY};
	}
	
	this.shapeCenterToBasePoint=function(x,y) {
		return {
			x: x-this.cellSize/2, 
			y: y-this.cellSize/2
			}
	}
	
	this.getCellPoint=function(row,col) {
	    return {
	        x: row*this.cellSize,
	        y: col*this.cellSize
	    }
	}
	
	this.shapes={
	    "empty": new GridSquare_ShapeEmpty(this),
		"flat": new GridSquare_ShapeFlat(this),
		"diamond": new GridSquare_ShapeDiamond(this),
		"jewel": new GridSquare_ShapeJewel(this)
	}
}
