% Projection and Unprojection with MATLAB from inverse depth
syms cx cy fx fy tx real
syms Px Py Pz real
syms px py invdepth real
dividew4 = @(P) P/P(4);
dividew3 = @(P) P/P(4);

K = [fx 0 cx; 0 fy cy; 0 0 1];
K4 = [fx 0 0 cx; 0 fy 0 cy; 0 0 0 1; 0 0 1 0];
Rt = sym(eye(4));
Rt(1,4) = tx;

P = K4*Rt;
iP = inv(P);
pidepth2dto3d = @(p) dividew4(iP*p);
p3dtoidepth2 = @(p) dividew4(P*p);

pi = [px py invdepth 1]';
piw = iP*pi;
piw3 = simplify(dividew4(piw));

% reverse
pw = [Px Py Pz 1]';
pwi = P*pw;
pwi3 = simplify(dividew4(pwi))

% verify

piw3i = simplify(p3dtoidepth2(piw3))
pwi3w = simplify(pidepth2dto3d(pwi3))
