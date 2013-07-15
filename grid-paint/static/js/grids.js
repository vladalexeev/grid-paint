function GridSquare() {
	this.cellSize=24;
	this.paintGrid=function (paper) {
		for (var y=0; y<(paper.height-this.cellSize); y+=this.cellSize) {
			for (var x=0; x<(paper.width-this.cellSize); x+=this.cellSize) {
				var r=paper.rect(x, y, this.cellSize, this.cellSize);
				r.attr({
					"fill":"#ffffff",
					"stroke": "#808080"
					});
			}			
		}
	}
}

function GridTriangle () {
	this.cellSize=24;
	this.paintGrid=function (paper) {
		var rowHeight=this.cellSize*Math.sin(60/180*Math.PI);
		for (var y=0; y<(paper.height-rowHeight); y+=rowHeight) {
			for (var x=0; x<(paper.width-this.cellSize*1.5); x+=this.cellSize) {
				var path1=paper.path(
					"M "+x+" "+(y+rowHeight)+" L "+(x+this.cellSize/2)+" "+y+
					" L "+(x+this.cellSize)+" "+(y+rowHeight)+" Z");
				path1.attr({
					"fill":"#ffffff",
					"stroke": "#808080"
					});
					
				var path2=paper.path(
					"M "+(x+this.cellSize/2)+" "+y+" L "+(x+this.cellSize)+" "+(y+rowHeight)+
					" L "+(x+this.cellSize*1.5)+" "+y+" Z"
				);
				path2.attr({
					"fill":"#ffffff",
					"stroke": "#808080"
					});
			}
		}
	}
}
