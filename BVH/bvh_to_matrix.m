function [ data, jointNames, dt, skeletonText ] = bvh_to_matrix( fname )
% Aline Normoyle, 2013
%   number of dimensions = number of columns 
%       = (#joints * #dofsPerJoint)
%   number of rows = number of frames
% Be careful: numDofPerJoint will differ between files, we hardcode 6 here!

fid=fopen(fname, 'rt');
if fid == -1,
 fprintf('Error, can not open file %s.\n', fname);
 return;
end;

jointNames = {};
skeletonText = {};

% read-in header
line=fgetl(fid);
while ~strcmp(line,'HIERARCHY')
  line=fgetl(fid);
end

% read-in skeleton
line=fgetl(fid);
while ~strcmp(line,'MOTION')
  length = size(line,2);
  
  idx = findstr(line, 'ROOT');
  if size(idx,1) ~= 0
      jointNames{end+1} = line(:,idx+5:length);
  end
  
  idx = findstr(line, 'JOINT');
  if size(idx,1) ~= 0
      jointNames{end+1} = line(:,idx+6:length);
  end
  skeletonText{end+1} = line;
  line=fgetl(fid);
end

numframes = fscanf(fid,'Frames: %d');
line=fgetl(fid);
dt = fscanf(fid,'Frame Time: %f');
line = fgetl(fid);

numchannels = numel(jointNames)*6;
data = zeros(numframes, numchannels);
for i = 1:numframes
    line = fgetl(fid);
    [token, remain] = strtok(line);    
    for j = 1:numchannels
        data(i,j) = str2num(token);
        [token,remain] = strtok(remain);
    end
end

fclose(fid);

end

