from datasets import load_dataset
from transformers import MarianMTModel, MarianTokenizer
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

# 加载WMT数据集，中文到英文
dataset = load_dataset('wmt19', 'zh-en')

# 加载预训练的MarianMT模型和分词器（中文到英文）
model_name = 'Helsinki-NLP/opus-mt-zh-en'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# 训练函数
def train_translation_model(train_dataset, model, tokenizer):
    # 定义训练参数
    training_args = Seq2SeqTrainingArguments(
        per_device_train_batch_size=4,
        evaluation_strategy="epoch",
        logging_dir='./logs',
        logging_steps=100,
        save_steps=1000,
        eval_steps=1000,
        num_train_epochs=3,
        overwrite_output_dir=True,
    )

    # 实例化Trainer对象
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
    )

    # 开始训练
    trainer.train()

# 示例调用
train_translation_model(dataset['train'], model, tokenizer)

# 进行推理函数
def translate_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

# 示例翻译
chinese_text = "你好，最近怎么样？"
translated_text = translate_text(chinese_text, model, tokenizer)
print("Translated text:", translated_text)
