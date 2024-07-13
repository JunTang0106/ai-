<template>
  <div class="voice-translator">
    <h1>唐俊的基于百度api语音识别和翻译网站</h1>
    <div class="controls">
      <button @click="startRecording" :disabled="isRecording">开始录音</button>
      <button @click="stopRecording" :disabled="!isRecording">结束录音</button>
      <button @click="startRecognition" :disabled="!audioBlob">开始识别</button>
      <button @click="startTranslation" :disabled="!recognizedText">开始翻译</button>
    </div>
    <div class="results">
      <div v-if="recognizedText">
        <h2>识别结果</h2>
        <textarea v-model="recognizedText" readonly></textarea>
      </div>
      <div v-if="translatedText">
        <h2>翻译结果</h2>
        <textarea v-model="translatedText" readonly></textarea>
      </div>
    </div>
  </div>
</template>

<script>
import { recognizeSpeech, translateText } from '@/api';

export default {
  data() {
    return {
      audioBlob: null,
      recognizedText: '',
      translatedText: '',
      isRecording: false,
      mediaRecorder: null,
      audioChunks: [],
    };
  },
  methods: {
    async startRecording() {
      this.isRecording = true;
      this.audioChunks = [];
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };
        this.mediaRecorder.start();
      } catch (error) {
        console.error('Error accessing microphone:', error);
        this.isRecording = false;
      }
    },
    stopRecording() {
      this.isRecording = false;
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
        this.mediaRecorder.onstop = () => {
          this.audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
        };
      }
    },
    async startRecognition() {
      if (!this.audioBlob) return;
      const response = await recognizeSpeech(this.audioBlob);
      if (response.result) {
        this.recognizedText = response.result[0];
      } else {
        alert('语音识别失败');
      }
    },
    async startTranslation() {
      if (!this.recognizedText) return;
      console.log('开始翻译，文本:', this.recognizedText);
      const response = await translateText(this.recognizedText);
      console.log('翻译响应:', response);
      if (response.result && response.result.trans_result && response.result.trans_result.length > 0) {
        this.translatedText = response.result.trans_result[0].dst;
      } else {
        alert('翻译失败');
      }
    }
  }
};
</script>

<style scoped>
.voice-translator {
  max-width: 600px;
  margin: 20px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}
.controls {
  margin-bottom: 20px;
}
button {
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.results {
  margin-top: 20px;
}
textarea {
  width: 100%;
  height: 100px;
  margin-top: 10px;
  font-size: 16px;
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  resize: none;
}
</style>
