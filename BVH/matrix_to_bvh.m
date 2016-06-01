function [] = matrix_to_bvh( fname, data, dt, skeleton )
% Aline Normoyle, 2013
%   number of dimensions = number of columns 
%       = rootTranslationXYZ+(#joints * #dofsPerJoint)
%   number of rows = number of frames

fid=fopen(fname, 'wt');
if fid == -1,
 fprintf('Error, can not open file %s.\n', fname);
 return;
end;

fprintf(fid,sprintf('%s', 'HIERARCHY\n'));
for i=1:size(skeleton,2)
    fprintf(fid, sprintf('%s\n',skeleton{i}));    
end
fprintf(fid, sprintf('MOTION\n'));
fprintf(fid, sprintf('Frames: %d\n', size(data,1)));
fprintf(fid, sprintf('Frame Time: %f\n', dt));
for i=1:size(data,1)
    for j=1:size(data,2)
        fprintf(fid, sprintf('%f ', data(i,j)));
    end
    fprintf(fid, sprintf('\n'));
end
fclose(fid);

end
