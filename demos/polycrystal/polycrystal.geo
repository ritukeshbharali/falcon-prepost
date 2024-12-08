//SetFactory("OpenCASCADE");

a  = 1.0;
lc = 0.01;

Point(1) = {0.0, 0, 0, lc};
Point(2) = {0.24, 0, 0, lc};
Point(3) = {0.35, 0, 0, lc};
Point(4) = {0.64, 0, 0, lc};
Point(5) = {0.94, 0, 0, lc};
Point(6) = {1.0, 0, 0, lc};
Point(7) = {1.0, 0.08, 0, lc};
Point(8) = {1.0, 0.4, 0, lc};
Point(9) = {1.0, 0.57, 0, lc};
Point(10) = {1.0, 1.0, 0, lc};
Point(11) = {0.94, 1.0, 0, lc};
Point(12) = {0.64, 1.0, 0, lc};
Point(13) = {0.35, 1.0, 0, lc};
Point(14) = {0.24, 1.0, 0, lc};
Point(15) = {0.0, 1.0, 0, lc};
Point(16) = {0.0, 0.57, 0, lc};
Point(17) = {0.0, 0.4, 0, lc};
Point(18) = {0.0, 0.08, 0, lc};

Point(19) = {0.0505, 0.091, 0, lc};
Point(20) = {0.1665, 0.077, 0, lc};
Point(21) = {0.67, 0.226, 0, lc};
Point(22) = {0.705, 0.190, 0, lc};
Point(23) = {0.9730, 0.061, 0, lc};

Point(24) = {0.1, 0.59, 0, lc};
Point(25) = {0.34, 0.41, 0, lc};
Point(26) = {0.58, 0.46, 0, lc};
Point(27) = {0.61, 0.442, 0, lc};
Point(28) = {0.97, 0.55, 0, lc};

Point(29) = {0.27, 0.97, 0, lc};
Point(30) = {0.3, 0.92, 0, lc};
Point(31) = {0.55, 0.76, 0, lc};
Point(32) = {0.88, 0.85, 0, lc};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {5,6};

Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};

Line(10) = {10,11};
Line(11) = {11,12};
Line(12) = {12,13};
Line(13) = {13,14};
Line(14) = {14,15};

Line(15) = {15,16};
Line(16) = {16,17};
Line(17) = {17,18};
Line(18) = {18,1};

Line(19) = {18,19};
Line(20) = {19,20};
Line(21) = {20,2};
Line(22) = {3,21};
Line(23) = {21,22};
Line(24) = {4,22};
Line(25) = {5,23};
Line(26) = {22,23};
Line(27) = {23,7};

Line(28) = {17,19};
Line(29) = {20,25};
Line(30) = {27,21};
Line(31) = {28,8};

Line(32) = {16,24};
Line(33) = {24,25};
Line(34) = {25,26};
Line(35) = {26,27};
Line(36) = {27,28};
Line(37) = {28,9};

Line(38) = {24,30};
Line(39) = {30,31};
Line(40) = {31,26};

Line(41) = {31,32};
Line(42) = {32,9};
Line(43) = {14,29};
Line(44) = {29,30};
Line(45) = {29,13};
Line(46) = {31,12};
Line(47) = {32,11};

Line Loop(101)     = {1,-21,-20,-19,18};     
Plane Surface(101) = {101};
Line Loop(102)     = {5,6,-27,-25};          
Plane Surface(102) = {102};
Line Loop(103)     = {42,9,10,-47};          
Plane Surface(103) = {103};
Line Loop(104)     = {32,38,-44,-43,14,15};  
Plane Surface(104) = {104};

Line Loop(105)     = {40,35,36,37,-42,-41};  
Plane Surface(105) = {105};

Line Loop(106)     = {4,25,-26,-24};
Plane Surface(106) = {106};
Line Loop(107)     = {41,47,11,-46};
Plane Surface(107) = {107};

Line Loop(108)     = {20,29,-33,-32,16,28};
Plane Surface(108) = {108};
Line Loop(109)     = {8,-37,31};
Plane Surface(109) = {109};

Line Loop(110)     = {2,22,-30,-35,-34,-29,21};
Plane Surface(110) = {110};
Line Loop(111)     = {45,13,43};
Plane Surface(111) = {111};

Line Loop(112)     = {33,34,-40,-39,-38};
Plane Surface(112) = {112};

Line Loop(113)     = {26,27,7,-31,-36,30,23};
Plane Surface(113) = {113};
Line Loop(114)     = {17,19,-28};
Plane Surface(114) = {114};

Line Loop(115)     = {3,24,-23,-22};
Plane Surface(115) = {115};
Line Loop(116)     = {39,46,12,-45,44};
Plane Surface(116) = {116};

Physical Line("Bottom")      = {1,2,3,4,5};
Physical Line("Right")       = {6,7,8,9};
Physical Line("Top")         = {10,11,12,13,14};
Physical Line("Left")        = {15,16,17,18};
Physical Line("Internal")    = {19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47};

Physical Surface("Domain1") = {105};
Physical Surface("Domain2") = {101,102,103,104};
Physical Surface("Domain3") = {106,107};
Physical Surface("Domain4") = {108,109};
Physical Surface("Domain5") = {110,111};
Physical Surface("Domain6") = {112};
Physical Surface("Domain7") = {113,114};
Physical Surface("Domain8") = {115,116};

Mesh 2;
Save "polycrystal.msh";
