import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

export const recognizeSpeech = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob);

    console.log('语音识别请求参数:', formData);

    const response = await axios.post(`${BASE_URL}/recognize`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    console.log('语音识别响应:', response.data);

    return response.data;
};

export const translateText = async (text) => {
    console.log('翻译请求参数:', { text });

    const response = await axios.post(`${BASE_URL}/translate`, { text });

    console.log('翻译响应:', response.data);

    return response.data;
};
