SetFactory("OpenCASCADE");

a   = 0.5;
l0  = 0.015;
h   = l0/4;
lc  = l0;

Point(1) = {-a, -a, 0, lc};
Point(2) = {a, -a, 0, h};
Point(3) = {a, a, 0, lc};
Point(4) = {-a, a, 0, lc};
Point(5) = {-a, h/2, 0, lc};
Point(6) = {0, h/2, 0, lc};
Point(7) = {0, -h/2, 0, h};
Point(8) = {-l0, -h/2, 0, h};
Point(9) = {-a, -h/2, 0, lc};
Point(10) = {2*l0, -h/2, 0, h};
Point(11) = {a, -h/2, 0, h};
Point(12) = {-l0, -a, 0, h};

Line(1) = {1,12};
Line(2) = {12,2};
Line(3) = {2,11};
Line(4) = {11,3};
Line(5) = {3,4};
Line(6) = {4,5};
Line(7) = {5,6};
Line(8) = {6,7};
Line(9) = {7,8};
Line(10) = {8,9};
Line(11) = {9,1};
Line(12) = {7,10};
Line(13) = {10,11};
Line(14) = {12,8};

Line Loop(101) = {1,14,10,11};         Plane Surface(101) = {101};
Line Loop(102) = {4,5,6,7,8,12,13};    Plane Surface(102) = {102};
Line Loop(103) = {2,3,-13,-12,-9,-14}; Plane Surface(103) = {103};

Recombine Surface {101};
Recombine Surface {102};
Recombine Surface {103};

Physical Line("Bottom") = {1,2};
Physical Line("Right")  = {3,4};
Physical Line("Top")    = {5};
Physical Line("Left")   = {6,11};

Physical Surface("Domain") = {101,102,103};

Mesh 2;
Save "sens.msh";