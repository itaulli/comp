"""
This module assists in setting up boundary conditions for 2-d PDEs
"""

__author__="Igor Volobouev (i.volobouev@ttu.edu)"
__version__="0.1"
__date__ ="Mar 07 2016"

import math
import numpy as np

# Overlap of two intervals [a, b] and [c, d], with integer a, b, c, d.
# The code assumes that a <= b and c <= d.
def _overlap(interval1, interval2):
    lmin, lmax = interval1
    rmin, rmax = interval2
    if (lmax == rmin):
        return (lmax, lmax)
    if (rmax == lmin):
        return (lmin, lmin)
    if (lmax > rmin and rmax > lmin):
        if lmin < rmin:
            omin = rmin
        else:
            omin = lmin
        if lmax < rmax:
            omax = lmax
        else:
            omax = rmax
        return (omin, omax)
    return (0, -1)


class GridFill2d:
    """
    This class can be used to define boundary conditions for 2-d PDEs.

    This class associates a rectangular grid with a coordinate system.
    The origin of this system is placed at the bottom left corner of
    the grid. Using the system coordinates, one can "draw" boundary
    conditions with the help of class methods "setPoint", "setLine",
    "setRectangle", "fillRectangle", "setCircle", and "setArc".
    """
    def __init__(self, nx, xmin, xmax, ny, ymin, ymax, initialValue, reverseRows=False):
        """
        Constructor arguments are as follows:

        nx           -- Number of grid points in the X direction

        xmin, xmax   -- X coordinates of the leftmost and the rightmost
                        grid points

        ny           -- Number of grid points in the Y direction

        ymin, ymax   -- Y coordinates of the lowest and the highest
                        grid points

        initialValue -- Initial value to give to all grid points. You
                        can initialize the grid points to some special
                        value (e.g., a very large number) which will be
                        later understood by your code as absence of
                        boundary conditions for these points.

        reverseRows  -- If True, the row numbers will be reversed, i.e.,
                        higher row numbers will correspond to smaller Y
                        coordinates. This is useful if the array will be
                        displayed by "matshow" or other matplotlib functions
                        which place the first row of the array at the top
                        of the plot.
        """
        assert nx > 1
        assert ny > 1
        self.nx = nx
        self.xmin = xmin*1.0
        self.xmax = xmax*1.0
        self.ny = ny
        self.ymin = ymin*1.0
        self.ymax = ymax*1.0
        self.data = (initialValue*1.0)*np.ones((ny, nx), np.float64)
        self.reverseRows = reverseRows
        self._dx = (self.xmax - self.xmin)/(nx - 1)
        self._dy = (self.ymax - self.ymin)/(ny - 1)
        self.invalidIndex = (-1, -1)
    
    def _closestIndex(self, x, y):
        xcell = int(round((x - self.xmin)/self._dx))
        ycell = int(round((y - self.ymin)/self._dy))
        if (xcell >= 0 and xcell < self.nx and ycell >= 0 and ycell < self.ny):
            return (xcell, ycell)
        else:
            return self.invalidIndex
    
    def _setPointFromGridCoords(self, xc, yc, value):
        xcell = int(round(xc))
        ycell = int(round(yc))
        if (xcell >= 0 and xcell < self.nx and ycell >= 0 and ycell < self.ny):
            if self.reverseRows:
                self.data[self.ny - ycell - 1, xcell] = value
            else:
                self.data[ycell, xcell] = value
            return True
        else:
            return False
    
    def _setVertical(self, x, y0, y1, value):
        xc = int(round((x - self.xmin)/self._dx))
        if xc >= 0 and xc < self.nx:
            y0c = int(round((y0 - self.ymin)/self._dy))
            y1c = int(round((y1 - self.ymin)/self._dy))
            ybegin, yend = _overlap(sorted((y0c, y1c)), (0, self.ny-1))
            for iy in range(ybegin, yend+1):
                if self.reverseRows:
                    self.data[self.ny - iy - 1, xc] = value
                else:
                    self.data[iy, xc] = value
            return y0c >= 0 and y0c < self.ny and \
                   y1c >= 0 and y1c < self.ny
        else:
            return False
    
    def _setHorizontal(self, x0, x1, y, value):
        yc = int(round((y - self.ymin)/self._dy))
        if yc >= 0 and yc < self.ny:
            if self.reverseRows:
                yc = self.ny - yc - 1
            x0c = int(round((x0 - self.xmin)/self._dx))
            x1c = int(round((x1 - self.xmin)/self._dx))
            xbegin, xend = _overlap(sorted((x0c, x1c)), (0, self.nx-1))
            for ix in range(xbegin, xend+1):
                self.data[yc, ix] = value
            return x0c >= 0 and x0c < self.nx and \
                   x1c >= 0 and x1c < self.nx
        else:
            return False
    
    def setPoint(self, x, y, value):
        """
        This function finds a point in the grid closest to the (x, y)
        location. This point will be found if (x, y) is inside the
        grid boundaries or not too far outside (less than half of the
        grid cell size beyond the boundary). If the point is found,
        it is set to the given value and the function returns "True".
        If the point is not found, the grid is not changed and the
        function returns "False".
        """
        ix, iy = self._closestIndex(x, y)
        if (ix, iy) == self.invalidIndex:
            return False
        else:
            if self.reverseRows:
                self.data[self.ny - iy - 1, ix] = value
            else:
                self.data[iy, ix] = value
            return True
    
    def setLine(self, x0, y0, x1, y1, value):
        """
        This function sets all grid points along the straight line
        drawn from (x0, y0) to (x1, y1) to the given value. "True"
        is returned if the whole line is situated inside the grid
        boundary.
        """
        if y0 == y1:
            return self._setHorizontal(x0, x1, y1, value)
        if x0 == x1:
            return self._setVertical(x0, y0, y1, value)
        x0c = (x0 - self.xmin)/self._dx
        x1c = (x1 - self.xmin)/self._dx
        y0c = (y0 - self.ymin)/self._dy
        y1c = (y1 - self.ymin)/self._dy
        dx = x1c - x0c
        dy = y1c - y0c
        len = math.sqrt(dx*dx + dy*dy)
        status = True
        if len > 0.0:
            nsteps = int(len*10 + 1)
            step = len/nsteps
            cos_x = dx/len
            cos_y = dy/len
            for i in range(nsteps):
                ds = step*i
                s = self._setPointFromGridCoords(x0c+cos_x*ds, y0c+cos_y*ds, value)
                status = status and s
        s = self._setPointFromGridCoords(x1c, y1c, value)
        return status and s
    
    def setRectangle(self, x0, y0, x1, y1, value):
        """
        This function sets all grid points along the perimeter of
        the rectangle with corners at (x0, y0) and (x1, y1) to the
        given value. "True" is returned if the whole rectangle is
        situated inside the grid boundary.
        """
        s0 = self.setLine(x0, y0, x0, y1, value)
        s1 = self.setLine(x0, y1, x1, y1, value)
        s2 = self.setLine(x1, y1, x1, y0, value)
        s3 = self.setLine(x1, y0, x0, y0, value)
        return s0 and s1 and s2 and s3
    
    def fillRectangle(self, x0, y0, x1, y1, value):
        """
        This function sets all grid points along the perimeter and
        inside the rectangle with corners at (x0, y0) and (x1, y1) to
        the given value. "True" is returned if the whole rectangle is
        situated inside the grid boundary.
        """
        x0c = int(round((x0 - self.xmin)/self._dx))
        x1c = int(round((x1 - self.xmin)/self._dx))
        y0c = int(round((y0 - self.ymin)/self._dy))
        y1c = int(round((y1 - self.ymin)/self._dy))
        xbegin, xend = _overlap(sorted((x0c, x1c)), (0, self.nx-1))
        ybegin, yend = _overlap(sorted((y0c, y1c)), (0, self.ny-1))
        for ix in range(xbegin, xend+1):
            for iy in range(ybegin, yend+1):
                if self.reverseRows:
                    self.data[self.ny - iy - 1, ix] = value
                else:
                    self.data[iy, ix] = value
        return x0c >= 0 and x0c < self.nx and \
               x1c >= 0 and x1c < self.nx and \
               y0c >= 0 and y0c < self.ny and \
               y1c >= 0 and y1c < self.ny

    def setCircle(self, xcenter, ycenter, radius, value):
        """
        This function sets all grid points along the circle with the
        given center and radius to the given value. "True" is returned
        if the whole circle is situated inside the grid boundary.
        """
        return self.setArc(xcenter, ycenter, radius, 0.0, 360.0, value)

    def setArc(self, xcenter, ycenter, radius, beginAngleDeg, endAngleDeg, value):
        """
        This function sets all grid points along the arc with the
        given center, radius, starting angle, and stopping angle
        to the given value. "True" is returned if the whole arc
        is situated inside the grid boundary. The angle arguments
        should be provided in degrees.
        """
        assert radius >= 0.0
        if radius == 0.0:
            return self.setPoint(xcenter, ycenter, value)
        beginAngle = beginAngleDeg/180.0*math.pi
        endAngle = endAngleDeg/180.0*math.pi
        da = min(self._dx, self._dy)/radius/10.0
        nsteps = int(abs(beginAngle - endAngle)/da + 1)
        da = (endAngle - beginAngle)/nsteps
        status = True
        for ia in range(nsteps):
            a = beginAngle + ia*da
            x = xcenter + radius*math.cos(a)
            y = ycenter + radius*math.sin(a)
            s = self.setPoint(x, y, value)
            status = status and s
        x = xcenter + radius*math.cos(endAngle)
        y = ycenter + radius*math.sin(endAngle)        
        s = self.setPoint(x, y, value)
        return status and s
