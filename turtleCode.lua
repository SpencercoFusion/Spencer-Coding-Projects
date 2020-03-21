xstart = 0
ystart = 0
zstart = 0
x = xstart
y = ystart
z = zstart

function xor(arg1, arg2)
    output = (arg1 or arg2) and not (arg1 and arg2)
    return(output)
end

function dump(o)
    if type(o) == 'table' then
       local s = '{ '
       for k,v in pairs(o) do
          if type(k) ~= 'number' then k = '"'..k..'"' end
          s = s .. '['..k..'] = ' .. dump(v) .. ','
       end
       return s .. '} '
    else
       return tostring(o)
    end
 end    

function DefineCircle(radius)
    CirclePoints = {}
    totalBlocks = 0

    yc = radius
    xc = 0
    for x=0, radius do
        for y=0, radius do
            if xor(dist(x + 0.5, y + 0.5, xc, yc) > radius, dist(x - 0.5, y - 0.5, xc, yc) > radius) then 
                radians = math.atan((y - yc), (x - xc))
                CirclePoints['x' .. totalBlocks] = x
                CirclePoints['y' .. totalBlocks] = y
                totalBlocks = totalBlocks + 1
            elseif xor(dist(x - 0.5, y + 0.5, xc, yc) > radius, dist(x + 0.5, y - 0.5, xc, yc) > radius) then 
                radians = math.atan((y - yc), (x - xc))
                CirclePoints['x' .. totalBlocks] = x
                CirclePoints['y' .. totalBlocks] = y                
                totalBlocks = totalBlocks + 1      
            end
        end
    end
    print(dump(CirclePoints))
    print(totalBlocks)

end

function dist(x1, y1, x2, y2)
    distance = math.sqrt((x1-x2)^2 + (y1-y2)^2)
    return(distance)
end

function moveTo(xG, yG)
    while x ~= xG and y ~= yG do
        if x < xG then
            if turtle.forward() then
                x = x + 1
            end
        elseif x > xG then
            if turtle.back() then
                x = x - 1
            end
        end
        if y < xG then
            if turtle.left() then
                y = y + 1
            end
        elseif y > yG then
            if turtle.right() then
                y = y - 1
            end
        end
    end 
end

DefineCircle(30)

for i=0, totalBlocks - 1 do
    x = CirclePoints['x' .. i]
    y = CirclePoints['y' .. i]
    print('number ' .. i .. ': ' .. x .. ' ' .. y)
end