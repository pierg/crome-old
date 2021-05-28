function _n(val, def) {
  return (typeof val === 'number') ? val : def;
}

const floor = Math.floor;

function Node(x, y, backgroundColor) {
  this.x = x;
  this.y = y;
  this.backgroundColor = backgroundColor || null;
  this.blocked = false;
}

Node.prototype = {
  toString: function() {
    return "<node x=" + this.x + " y=" + this.y + " blocked=" + this.blocked + ">";
  }
}

function GridWorld(canvas, width, height, options) {

  options = options || {};

  this.canvas  = canvas;
  this.ctx     = canvas.getContext('2d');
  this.width   = floor(width) * 2 ;
  this.height  = floor(height) * 2 ;

  let padding = options.padding;

  if (typeof padding === 'undefined') {
    padding = 0;
  }

  if (typeof padding === 'number') {
    this.padding = {
      top     : padding,
      right   : padding,
      bottom  : padding,
      left    : padding
    };
  } else {
    this.padding = padding;
  }

  this.cellSize = _n(options.cellSize, 25);
  this.cellSizeWall = _n(options.cellSize, 5);
  this.cellSpacing = _n(options.cellSpacing, 2);
  this.drawBorder = !!options.drawBorder;
  this.borderColor = options.borderColor || 'lightgrey';
  this.backgroundColor = options.backgroundColor || 'white';

  if (options.resizeCanvas) {
    let cw = this.padding.left + this.padding.right,
        ch = this.padding.top + this.padding.bottom;
    cw += ((this.width) * (this.cellSize +  this.cellSizeWall + this.cellSpacing));
    ch += ((this.height) * (this.cellSize + this.cellSizeWall + this.cellSpacing)) -  2 * this.cellSize;

    if (this.drawBorder) {
      cw += (this.cellSpacing * 2);
      ch += (this.cellSpacing * 2);
    }
    this.canvas.width = cw;
    this.canvas.height = ch;
  }

  this.nodes = [];
  for (let j = 0; j < this.height + 1; ++j) {
    for (let i = 0; i < this.width + 1; ++i) {
      this.nodes.push(new Node( i,j, null));
    }
  }

  //
  // Event handling
  // TODO: support dragging

  const self = this;

  this.onclick = options.onclick;

  function p2n(x, y) {

    x -= self.padding.left;
    y -= self.padding.top;

    if (self.drawBorder) {
      x -= (self.cellSpacing * 2);
      y -= (self.cellSpacing * 2);
    }
    let a = 2 * self.cellSpacing + 2 * self.cellSizeWall;
    const tabX = [a]; // array that gives the pixel from which we change nodes from the x-coordinate
    const tabY = [a]; // array that gives the pixel from which we change nodes from the y-coordinate

    for (let i = 0; i < self.width; i += 2) {
      a += 2 * self.cellSize;
      tabX.push(a);
      tabY.push(a);

      a += 2 * self.cellSizeWall + self.cellSpacing;
      tabX.push(a);
      tabY.push(a);
      a += self.cellSpacing;
    }
    let indexX = 0;
    if (x > tabX[0]) {
      indexX = 1;
    }
    while (x >= tabX[indexX] ) { // find out in which interval the clicked pixel is located from the x-coordinate
      indexX++;
    }
    let indexY = 0;
    if (y > tabY[0]) {
      indexY = 1;
    }
    while (y >= tabY[indexY] ) { // find out in which interval the clicked pixel is located from the y-coordinate
      indexY++;
    }

    if (indexX >= 0 && indexX < self.width + 3 * self.cellSizeWall && indexY >= 0 && indexY < self.height + 3 * self.cellSizeWall) { // associates the clicked pixel with a node
      return self.nodes[(indexY * (self.width + 1)) + indexX];
    }
    else {
      return null;
    }
  }
  let start =[];
  let end =[];
  let startWall =[];
  let endWall =[];
  let previousColorWall;
  let previousStartColor;
  let previousEndColor;

  canvas.addEventListener('click', function(evt) {

    if (!self.onclick)
      return;

    const node = p2n(evt.offsetX, evt.offsetY);

    if (node) {
      if (node.x % 2 === 1 && node.y % 2 === 1) { // when you click on a cell
        if (start.length === 0) {// if it's the first click on a cell, push into start table which represent the coordinated of the first click
          previousStartColor = self.getBackgroundColor(node.x, node.y); // save the color a the clicked cell
          start.push(node.x);
          start.push(node.y);
          if (self.onclick(node, start, end, startWall, endWall, previousStartColor, previousEndColor, previousColorWall) === false) { // if the user does anything that is not allowed
            start = [];
            end = [];
            startWall = [];
            endWall = [];
          }
        }
        else { // if it's the second click
          previousEndColor = self.getBackgroundColor(node.x, node.y); // save the color a the clicked cell
          if (startWall.length !== 0) { // if he clicks on a cell then a wall, it's not possible, the program cancel the actions
            self.setBackgroundColor(start[0],start[1], previousStartColor);
            self.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
            self.draw();
            start = [];
            startWall = [];

          }
          else {
            end.push(node.x);
            end.push(node.y);
            if (self.onclick(node, start, end, startWall, endWall, previousStartColor, previousEndColor, previousColorWall) === false) { // if the user does anything that is not allowed
              start = [];
              end = [];
              startWall = [];
              endWall = [];
            }
            start = [];
            end = [];
          }
        }
      }
      else if ((node.x % 2 === 1 && node.y % 2 === 0) || (node.x % 2 === 0 && node.y % 2 === 1)) {
        if (startWall.length === 0) { // if it's the first click on a wall, push into start table which represent the coordinated of the first click
          startWall.push(node.x);
          startWall.push(node.y);
          previousColorWall = self.getBackgroundColor(node.x, node.y); // save the color a the clicked wall
          self.onclick(node, start, end, startWall, endWall, previousStartColor, previousEndColor, previousColorWall);

        } else {
          if (start.length !== 0) { // if he clicks on a wall then a cell, it's not possible, the program cancel the actions
            self.setBackgroundColor(start[0],start[1], previousStartColor);
            self.setBackgroundColor(startWall[0],startWall[1], previousColorWall);
            self.draw();
            start = [];
            startWall = [];
          }
          else {
            endWall.push(node.x);
            endWall.push(node.y);
            self.onclick(node, start, end, startWall, endWall, previousStartColor, previousEndColor, previousColorWall);
            startWall = [];
            endWall = [];
          }
        }
      }
    }
  });

}

let idTable = [];

GridWorld.prototype = {
  draw: function() {

    let csz = this.cellSize,
        csz2 = this.cellSizeWall,
        csp = this.cellSpacing,
        ctx = this.ctx,
        ix = 0;

    const bAdj = this.drawBorder ? this.cellSpacing : -this.cellSpacing,
        cAdj = this.drawBorder ? this.cellSpacing : 0;

    ctx.save();
    ctx.fillStyle = this.borderColor;
    ctx.fillRect(this.padding.left,
        this.padding.top,
        (( csz + csz2 + csp) * this.width) + 2 *csz2 + 2 * csp + bAdj,
        ((csz + csz2 + csp) * this.height) + 2 *csz2 + 2 * csp + bAdj);

    let cy = this.padding.top + cAdj;
    for (let j = 0; j < this.height + 1; ++j) {
      let cx = this.padding.left + cAdj;
      for (let i = 0; i < this.width + 1; ++i) { // draw a wall and then a cell (size times) each wall or cell represent one node
        const n = this.nodes[ix++];
        ctx.fillStyle = n.backgroundColor || this.backgroundColor;
        if ( j % 2 === 1 ) {
          if (i % 2 === 1) {
            ctx.fillRect(cx, cy, 2 * csz, 2 * csz);
            cx += 2 * csz + csp;
          }
          else  {
            ctx.fillRect(cx, cy,2 * csz2, 2 * csz);
            cx += 2 * csz2 + csp;
          }
        }
        else {
          if (i % 2 === 1) {
            ctx.fillRect(cx, cy, 2 * csz, 2 * csz2);
            cx += 2 * csz + csp;
          }
          else  {
            ctx.fillRect(cx, cy, 2 * csz2, 2 * csz2);
            cx += 2 * csz2 + csp;
          }

        }
      }
      if (j % 2 === 1) {
        cy += 2 * csz + csp;
      }
      else {
        cy += 2 * csz2 + csp;
      }
    }

    ctx.restore();

  },

  get: function(x, y) {
    return this.nodes[(y * (this.width + 1)) + x];
  },

  getBackgroundColor: function(x, y) {
    return this.nodes[(y *  (this.width + 1)) + x].backgroundColor;
  },

  setBackgroundColor: function(x, y, color) {
    this.nodes[(y *  (this.width + 1)) + x].backgroundColor = color;
  },

  isBlocked: function(x, y) {
    return this.nodes[(y *  (this.width + 1)) + x].blocked;
  },

  setBlocked: function(x, y, blocked) {
    this.nodes[(y *  (this.width + 1)) + x].blocked = !!blocked;
  },

  setAttribute: function(x, y, key, value) {
    this.nodes[(y * (this.width + 1)) + x][key] = value;
    if (this.isAttribute(value) === false) { // if the value entered by the user has not already been selected, this value is added to the array :idTable
      idTable.push([value,this.getBackgroundColor(x,y)]);
    }
  },

  removeAttribute: function(value) {
    if (this.isID(value)) {
      for (let i = 0; i < this.width; i++) {
        for (let j = 0; j < this.height; j++) {
          if (this.getAttribute(i, j, "id") === value) {
            this.setBackgroundColor(i, j, "white");
            this.setBlocked(i, j, false);
          }
        }
      }
      this.clearAttribute(value);
      this.draw();
    }
  },

  isAttribute: function(value, color) { // checks if an id is in the array : idTable
       for (let i = 0; i < idTable.length ; i++) {
          if ((idTable[i][0] === value && idTable[i][1] !== color) || (idTable[i][0] !== value && idTable[i][1] === color)) {
            return true;
          }
       }
       return false;
  },

  isID : function(value) { // checks if an id is in the array : idTable
       for (let i = 0; i < idTable.length ; i++) {
          if (idTable[i][0] === value) {
            return true;
          }
       }
       return false;
  },
  clearAttribute: function(value) {
      let index = -1;
      for (let i = 0; i < idTable.length; i++) {
        if (idTable[i][0] === value) {
          index = i;
        }
      }
      let a = idTable[index];
      idTable[index] = idTable[idTable.length - 1];
      idTable[idTable.length - 1] = a;
      idTable.pop();
  },

  getAttribute: function(x, y, key) {
     return this.nodes[(y * (this.width + 1)) + x][key];
  },

  clearAttributeTable: function () {
    idTable = [];
  },

  checkNeighbour: function (i, j, color) {
    if (this.getBackgroundColor(i, j) !== color) {
      if (this.getBackgroundColor(i + 1, j) !== color && this.getBackgroundColor(i + 1, j) !== "black") {
        console.log(" i : " + i + " j : " + j + " in i+1 : " + this.getBackgroundColor( i + 1, j));
        this.setBackgroundColor(i + 1, j, "white");
        this.setBlocked(i + 1, j, false);

      }
      if (this.getBackgroundColor(i - 1, j) !== color && this.getBackgroundColor(i - 1, j) !== "black") {
        console.log(" i : " + i + " j : " + j + " in i-1 : " +this.getBackgroundColor(i - 1, j));
        this.setBackgroundColor(i - 1, j, "white");
        this.setBlocked(i - 1, j, false);

      }
      if (this.getBackgroundColor(i, j - 1) !== color && this.getBackgroundColor(i, j - 1) !== "black") {
        console.log(" i : " + i + " j : " + j + " in j-1 : " +  this.getBackgroundColor(i, j - 1));
        this.setBackgroundColor(i, j - 1, "white");
        this.setBlocked(i, j - 1, false);

      }
      if (this.getBackgroundColor(i, j + 1) !== color && this.getBackgroundColor(i, j + 1) !== "black") {
        console.log(" i : " + i + " j : " + j + " in j+1 : " +this.getBackgroundColor(i, j + 1));
        this.setBackgroundColor(i, j + 1, "white");
        this.setBlocked(i, j + 1, false);

      }
    }
  },

  setColorIdBlocked :function(i, j, color, blocked, id) {
    this.setBackgroundColor(i, j, color); // color the cell with the color choose by the user
    this.setBlocked(i, j, blocked);
    if (id !== null) {
      this.setAttribute(i, j, "id", id); // the cell has a attribute id which have a value of the input of the user
    }
  },

  min :function(x, y) {
    let min;
    let max;
    let answer = [];
    if (x < y) {
      min = x;
      max = y
    }
    else {
      min = y;
      max = x;
    }
    answer.push(min);
    answer.push(max);
    return answer;
  },

  eachNeighbour: function(x, y, callback) {
    return this.eachNodeNeighbour(this.nodes[(y *  (this.width + 1)) + x], callback);
  },

  eachNodeNeighbour: function(node, callback) {

    let x = node.x,
        y = node.y,
        w = this.width,
        h = this.height,
        ns = this.nodes,
        ix = (y * w) + x,
        nix = 0;

    if (x > 0   && !ns[ix-1].blocked) callback(ns[ix-1], nix++);
    if (x < w-1 && !ns[ix+1].blocked) callback(ns[ix+1], nix++);
    if (y > 0   && !ns[ix-w].blocked) callback(ns[ix-w], nix++);
    if (y < h-1 && !ns[ix+w].blocked) callback(ns[ix+w], nix++);

  },

  eachNode: function(callback) {
    this.nodes.forEach(callback);
  }

};


export default GridWorld;
