function totaldfc = disccashflow(cmoney,nyears, irate)
%FUNCTION_NAME - Functionthat calculate the discount cash flow
%
% Syntax:  output1 = function_name(input1,input2,input3)
%
% Inputs:
%    cmoney - current money value
%    nyears - number of years
%    irate - interest rate annualized
%
% Outputs:
%    output1 - Cash flow value for in
%    
%
% Example: 
%    http://www.investopedia.com/terms/d/dcf.asp
%    Line 2 of example
%    Line 3 of example
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
% Author: Jaime Gomez Ramirez
% December 2015; 

%------------- BEGIN CODE --------------

totaldfc = 0;
yeardfc = cmoney;
for i = 1:nyears
    yeardfc =  yeardfc / (1 + irate)^nyears
    totaldfc = yeardfc + totaldfc
end


%------------- END OF CODE --------------
