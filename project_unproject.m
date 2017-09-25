% Projection and Unprojection with MATLAB
syms cx cy fx fy tx real
syms Px Py Pz real
syms px py dis real
dividew4 = @(P) P/P(4);
dividew3 = @(P) P/P(4);

K = [fx 0 cx; 0 fy cy; 0 0 1];
K4 = [fx 0 0 cx; 0 fy 0 cy; 0 0 0 1; 0 0 1 0];
Rt = sym(eye(4));
Rt(1,4) = tx;

P = K4*Rt;
iP = inv(P);
pdis2dto3d = @(p) dividew4(iP*p);
p3dtodis2 = @(p) dividew4(P*p);

pi = [px py dis 1]';
piw = iP*pi;
piw3 = simplify(dividew4(piw));

% reverse
pw = [Px Py Pz 1]';
pwi = P*pw;
pwi3 = simplify(dividew4(pwi))

% verify

piw3i = simplify(p3dtodis2(piw3))
pwi3w = simplify(pdis2dto3d(pwi3))
