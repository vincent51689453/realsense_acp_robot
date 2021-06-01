class unsupCNN(nn.Moudle):
    def __init__(self,input_dim):
        super(unsupCNN,self).__init()
        #Input layer
        self.conv1 = nn.Conv2d(input_dim, hc.num_neurons_basic, kernel_size=hc.square_kernel_size, \
            stride=hc.stride_step, padding=hc.padding_approach)
        self.bn1 = nn.BatchNorm2d(hc.num_neurons_basic)

        # Create convolution and batchnormalization lists
        self.conv2 = nn.ModuleList()
        self.bn2 = nn.ModuleList()
        # Stack layers based on num_layers_basic
        for i in range(hc.num_layers_basic-1):
            self.conv2.append(nn.Conv2d(hc.num_neurons_basic, hc.num_neurons_basic, kernel_size=hc.square_kernel_size, \
                stride=hc.stride_step, padding=hc.padding_approach))
            self.bn2.append(nn.BatchNorm2d(hc.num_neurons_basic))
        
        # 1x1 convolution
        self.conv3 = nn.Conv2d(hc.num_neurons_basic,hc.num_neurons_basic, kernel_size=1, stride=1, padding=0 )
        self.bn3 = nn.BatchNorm2d(hc.num_neurons_basic)

    def forward(self,x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.bn1(x)
        for i in range(hc.num_layers_basic-1):
            x = self.conv2[i](x)
            x = F.relu( x )
            x = self.bn2[i](x)
        x = self.conv3(x)
        x = self.bn3(x)
        return x        