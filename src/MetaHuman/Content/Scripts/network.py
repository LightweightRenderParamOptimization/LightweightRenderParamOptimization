import torch
import torch.nn as nn
# import math
import matplotlib.pyplot as plt
import torch.nn.functional as F


# A dummy Positional Encoding module
class PositionalEncoding(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PositionalEncoding, self).__init__()
        self.fc = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        return self.fc(x)

# Define a custom Residual Block
class ResidualBlock(nn.Module):
    def __init__(self, input_dim):
        super(ResidualBlock, self).__init__()
        self.fc = nn.Linear(input_dim, input_dim)

    def forward(self, x):
        # Apply FC, add the input to the output (residual connection), then apply LReLU
        return F.leaky_relu(self.fc(x) + x)

# Define the custom Neural Network
class CustomNetwork(nn.Module):
    def __init__(self):
        super(CustomNetwork, self).__init__()
        # Positional Encoding module
        self.pos_enc = PositionalEncoding(5, 60)
        self.pos_enc2 = PositionalEncoding(5, 60)

        # Define the FC layers
        self.fc1 = nn.Linear(60, 256)  # For w and u after Positional Encoding
        self.fc2 = nn.Linear(512, 512) # After concatenation and before each Residual Block
        self.fc3 = nn.Linear(512, 256) # Before the final layer
        self.fc4 = nn.Linear(256, 5)   # Final layer to transform back to 3 dimensions
        self.fc5 = nn.Linear(5, 1)     # Final layer to transform to 1 dimension

        # Define Residual Blocks
        self.res_block1 = ResidualBlock(512)
        self.res_block2 = ResidualBlock(512)
        self.res_block3 = ResidualBlock(512)

    def forward(self, w, u):
        # Apply Positional Encoding and then FC1 + LReLU
        w_encoded = F.leaky_relu(self.fc1(self.pos_enc(w)))
        u_encoded = F.leaky_relu(self.fc1(self.pos_enc2(u)))

        # Concatenate the vectors
        concatenated = torch.cat((w_encoded, u_encoded), dim=1) # assuming dim=1 for concatenation

        # Apply FC + LReLU, followed by Residual Blocks
        x = F.leaky_relu(self.fc2(concatenated))
        x = F.leaky_relu(self.fc2(x))  # Additional FC + LReLU before the first Residual Block
        x = F.leaky_relu(self.fc2(self.res_block1(x)))
        x = F.leaky_relu(self.fc2(self.res_block2(x)))
        x = self.res_block3(x)  # The output from the last Residual Block

        # Add operation with the initial concatenated vector
        x = x + concatenated

        # Final transformations
        x = F.leaky_relu(self.fc3(x))
        x = F.leaky_relu(self.fc4(x))
        x = F.leaky_relu(self.fc5(x))
        x = F.mish(x)
        
        return x



# class PositionalEncoding(nn.Module):
#     def __init__(self, d_model, max_seq_len):
#         super(PositionalEncoding, self).__init__()
#         self.d_model = d_model
        
#         # 创建位置编码矩阵
#         pe = torch.zeros(max_seq_len, d_model)
#         position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)
#         div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
#         pe[:, 0::2] = torch.sin(position * div_term)
#         pe[:, 1::2] = torch.cos(position * div_term)
#         pe = pe.unsqueeze(0)
#         self.register_buffer('pe', pe)
        
#     def forward(self, x):
#         x = x + self.pe[:, :x.size(1)]
#         return x

# nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),
#             nn.Linear(512, 512),
#             nn.LeakyReLU(),

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(60, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 512),
            nn.LeakyReLU(),
            
            nn.Linear(512, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 5),
            nn.LeakyReLU(),
            nn.Linear(5, 1),
            nn.LeakyReLU(),
            nn.Mish()
            
        )

    def forward(self, x):
        x = self.fc(x)
        return x

def train_model(train_data1, train_data2, train_labels, batch_size = 200, num_epochs=2000, learning_rate=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CustomNetwork().to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # num_samples = len(train_data1)
    # num_batches = num_samples // batch_size

    losses = []

    for epoch in range(num_epochs):
    #     epoch_loss = 0.0

    #     for batch in range(num_batches):
    #         start_index = batch * batch_size
    #         end_index = start_index + batch_size
    #         inputs1 = torch.tensor(train_data1[start_index:end_index], dtype=torch.float32).to(device)
    #         inputs2 = torch.tensor(train_data2[start_index:end_index], dtype=torch.float32).to(device)
    #         labels = torch.tensor(train_labels[start_index:end_index], dtype=torch.float32).to(device).unsqueeze(1)

    #         optimizer.zero_grad()
    #         outputs = model(inputs1, inputs2)
    #         loss = criterion(outputs, labels)
    #         loss.backward()
    #         optimizer.step()
    #         epoch_loss += loss.item()

        inputs1 = torch.tensor(train_data1, dtype=torch.float32).to(device)
        inputs2 = torch.tensor(train_data2, dtype=torch.float32).to(device)
        labels = torch.tensor(train_labels, dtype=torch.float32).to(device).unsqueeze(1)

        optimizer.zero_grad()
        outputs = model(inputs1, inputs2)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        losses.append(loss.item())
            
        # losses.append(epoch_loss / num_batches)

        if (epoch + 1) % 50 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

    plt.plot(losses)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.show()

    return model