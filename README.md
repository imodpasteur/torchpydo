# Torchpydo

Torchpydo is a two-way bridge between Python/Numpy and Lua/Torch, allowing use using Torch packages(nn, rnn etc.) with numpy inside python.

This is a project inspired by lunatic-python and based on lunatic-python.

# Getting Start


## load torchpydo and bootstrap globals
``` python
import torchpydo as lua

# set the python globals() to lua, so you can update all lua global variables into python by default
lua.set_globals(globals())
lua.execute('greeting="hello world from lua"')
print(greeting)


# or if you don't want to mess the python global variables, you can skip the previous line, 
# but you need to access lua global variables through lua.globals(). 

# Note that if you do this, all the following code should change acorrdingly.

lg = lua.globals()
lua.execute('greeting="hello world from lua"')
print(lg.greeting)

```

## play with torch
``` python
lua.require("torch")
z = torch.Tensor(4,5,6,2)
print(torch.isTensor(z))

s = torch.LongStorage(6)
print(torch.type(s))
```

## load image and use nn module
``` python
# load image
lua.require("image")
img_rgb = image.lena()
print(img_rgb.size(img_rgb))
img = image.rgb2y(img_rgb)
print(img.size(img))

# use SpatialConvolution from nn to process the image
lua.require("nn")
n = nn.SpatialConvolution(1,16,12,12)
res = n.forward(n, img)
print(res.size(res))

```

# use Sequential model

``` python
mlp = nn.Sequential()

# bootstrap the add function to use add without passing self as the first arugment
lua.bs(mlp,'add')

module = nn.Linear(10, 5)
mlp.add(module)

print(module.weight)
print(module.bias)

print(module.gradWeight)
print(module.gradBias)

x = torch.Tensor(10) #10 inputs

# pass self to the function
y = mlp.forward(mlp, x)
print(y)

```


# Acknowledge

This is a project inspired by [lunatic-python](https://github.com/bastibe/lunatic-python) and based on lunatic-python.