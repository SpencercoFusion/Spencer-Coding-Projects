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
    file = io.open("circleTest.txt", "w")
    io.output(file)
    yc = radius
    xc = 0
    for x=0, radius do
        for y=0, radius do
            if xor(dist(x + 0.5, y + 0.5, xc, yc) > radius, dist(x - 0.5, y - 0.5, xc, yc) > radius) then 
                radians = math.atan((y - yc), (x - xc))
                io.write(x .. ' ' .. y .. ' ' .. radians .. '\n')
                CirclePoints[x .. ' ' .. y] = radians
                totalBlocks = totalBlocks + 1
            elseif xor(dist(x - 0.5, y + 0.5, xc, yc) > radius, dist(x + 0.5, y - 0.5, xc, yc) > radius) then 
                radians = math.atan((y - yc), (x - xc))
                io.write(x .. ' ' .. y .. ' ' .. radians .. '\n')
                CirclePoints[x .. ' ' .. y] = radians   
                totalBlocks = totalBlocks + 1      
            end
        end
    end
    file.close()
    print(dump(CirclePoints))
    print(totalBlocks)

end

function dist(x1, y1, x2, y2)
    distance = math.sqrt((x1-x2)^2 + (y1-y2)^2)
    return(distance)
end

function getNthLine(fileName, n)
    local f = io.open(fileName, "r")
    local count = 1

    for line in f:lines() do
        if count == n then
            f:close()
            return line
        end
        count = count + 1
    end

    f:close()
    error("Not enough lines in file!")
end

DefineCircle(30)

line = getNthLine("circleTest.txt", 1)
split("a b c", 'b')