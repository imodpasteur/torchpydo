# Torchpydo

Torchpydo is a two-way bridge between Python/Numpy and Lua/Torch, allowing use using Torch packages(nn, rnn etc.) with numpy inside python.

This is a project inspired by lunatic-python and based on lunatic-python.

# Installation
``` bash

git clone https://github.com/imodpasteur/torchpydo.git
cd torchpydo
python setup.py install     # use sudo if needed

```



# Getting Start


## import torchpydo and bootstrap globals
``` python
import torchpydo as lua
# set the python globals() to lua, so you can update all lua global variables into python by default
lua.set_globals(globals())
```
## hello world

``` python
lua.execute(' greeting = "hello world" ')
print(greeting)
```

### Note: alternative way to access lua globals
if you don't want to mess the python global variables, you can skip the previous line, but you need to access lua global variables through lua.globals(). 

Note that if you do this, all the following code should change acorrdingly.

``` python
import torchpydo as lua
lg = lua.globals()
lua.execute(' greeting = "hello world" ')
print(lg.greeting)

```

## execute lua code

``` python
a = lua.eval(' {11, 22} ') # define a lua table with two elements
print(a[1])

lua.execute(' b={33, 44} ') # define another lua table with two elements
print(b[0]) # will get None, because lua used 1 as first index
print(b[1])

```

## use torch
``` python
lua.require("torch")
z = torch.Tensor(4,5,6,2)
print(torch.isTensor(z))

s = torch.LongStorage(6)
print(torch.type(s))
```

## load image and use nn module
``` python
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

## build a simple model

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

## build another model and training it

Train a model to perform XOR operation.

``` python
lua.require("nn")
mlp = nn.Sequential()
lua.bs(mlp,'add')
mlp.add(nn.Linear(2, 20)) # 2 input nodes, 20 hidden nodes
mlp.add(nn.Tanh())
mlp.add(nn.Linear(20, 1)) # 1 output nodes

criterion = nn.MSECriterion() 

for i in range(2500):
    # random sample
    input= torch.randn(2)    # normally distributed example in 2d
    output= torch.Tensor(1)
    if input[1]*input[2] > 0:  # calculate label for XOR function
        output.fill(output,-1) # output[0] = -1
    else:
        output.fill(output,1) # output[0] = -1
    
    # feed it to the neural network and the criterion
    criterion.forward(criterion, mlp.forward(mlp, input), output)

    # train over this example in 3 steps
    # (1) zero the accumulation of the gradients
    mlp.zeroGradParameters(mlp)
    # (2) accumulate gradients
    mlp.backward(mlp, input, criterion.backward(criterion, mlp.output, output))
    # (3) update parameters with a 0.01 learning rate
    mlp.updateParameters(mlp, 0.01)

```
## test the model

``` python
x = torch.randn(2)
print(x)
yhat = mlp.forward(mlp,x)
print(yhat)
```



# Acknowledge

This is a project inspired by [lunatic-python](https://github.com/bastibe/lunatic-python) and based on lunatic-python.
