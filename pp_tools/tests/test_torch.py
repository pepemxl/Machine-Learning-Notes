import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GNN, self).__init__()
        # Define the first graph convolutional layer
        self.conv1 = GCNConv(in_channels, hidden_channels)
        # Define the second graph convolutional layer
        self.conv2 = GCNConv(hidden_channels, out_channels)
        # Define the linear layer
        self.linear = torch.nn.Linear(out_channels, out_channels)

    def forward(self, x, edge_index):
        # Apply the first graph convolutional layer
        x = self.conv1(x, edge_index)
        # Apply the ReLU activation function
        x = F.relu(x)
        # Apply the second graph convolutional layer
        x = self.conv2(x, edge_index)
        # Apply the ReLU activation function
        x = F.relu(x)
        # Apply the linear layer
        x = self.linear(x)
        # Apply the log softmax activation function
        return F.log_softmax(x, dim=1)