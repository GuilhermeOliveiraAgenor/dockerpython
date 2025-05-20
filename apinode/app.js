import express from 'express';
import axios from 'axios';
import { createClient } from 'redis';

const app = express();
app.use(express.json());

const URL = 'http://apipython:8000';

// Conecta ao Redis
const redisClient = createClient({
  url: 'redis://redis:6379'
});

redisClient.on('error', (err) => console.error('Redis Client Error', err));

await redisClient.connect();

app.get('/product', async (req, res) => {
  try {
    const cached = await redisClient.get('products');

    if (cached) {
      console.log('Cache hit');
      return res.json(JSON.parse(cached));
    }

    const response = await axios.get(`${URL}/product`);
    const data = response.data;

    await redisClient.set('products', JSON.stringify(data), {
      EX: 60
    });

    console.log('Dados vindos da API Python');
    res.json(data);
  } catch (error) {
    console.error('Erro ao acessar API Python:', error.message);
    res.status(500).json({ error: 'Erro ao acessar API Python' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API Node rodando na porta ${PORT}`);
});
