import os
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from torch.optim import Adam
import torch.nn as nn
from tqdm import tqdm
import soundfile as sf

# 定义处理器
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

# 加载模型
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# 定义数据集
class THCHS30Dataset(Dataset):
    def __init__(self, audio_dir, transcript_file, processor):
        self.audio_dir = audio_dir
        self.processor = processor
        self.transcripts = self.load_transcripts(transcript_file)
        self.audio_files = os.listdir(audio_dir)

    def load_transcripts(self, transcript_file):
        transcripts = {}
        with open(transcript_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    key, transcript = line.split(' ', 1)
                    transcripts[key] = transcript
        return transcripts

    def __len__(self):
        return len(self.audio_files)

    def __getitem__(self, idx):
        audio_file = self.audio_files[idx]
        audio_path = os.path.join(self.audio_dir, audio_file)
        key = audio_file.split('.')[0]
        transcript = self.transcripts[key]

        audio_input, _ = torchaudio.load(audio_path)
        input_values = self.processor(audio_input.squeeze(0), return_tensors="pt").input_values

        return input_values, transcript

# 训练函数
def train_model(model, train_loader, num_epochs=3):
    model.train()
    ctc_loss = nn.CTCLoss(blank=processor.tokenizer.pad_token_id)
    optimizer = Adam(model.parameters(), lr=1e-4)

    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        for batch in tqdm(train_loader, desc=f"Training"):
            optimizer.zero_grad()
            input_values = batch[0].squeeze(1)
            labels = processor.batch_encode_plus(batch[1], return_tensors="pt", padding=True)['input_ids']
            logits = model(input_values).logits
            log_probs = nn.functional.log_softmax(logits, dim=-1)
            input_lengths = torch.full(size=(input_values.size(0),), fill_value=input_values.size(1), dtype=torch.long)
            label_lengths = torch.tensor([len(label) for label in labels], dtype=torch.long)
            loss = ctc_loss(log_probs.permute(1, 0, 2), labels, input_lengths, label_lengths)
            loss.backward()
            optimizer.step()

# 推理函数
def transcribe_audio(audio_file):
    audio_input, sample_rate = sf.read(audio_file)
    input_values = processor(audio_input, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    return transcription[0]

if __name__ == "__main__":
    # 数据集路径和文件
    audio_dir = '../../THCHS-30'
    transcript_file = '../transcript'

    # 创建数据集和数据加载器
    dataset = THCHS30Dataset(audio_dir, transcript_file, processor)
    train_loader = DataLoader(dataset, batch_size=4, shuffle=True)

    # 训练模型
    train_model(model, train_loader)
