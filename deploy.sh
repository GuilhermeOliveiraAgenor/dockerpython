#!/bin/bash

echo "==========================================="
echo "Parando containers e removendo volumes..."
echo "==========================================="
docker compose down -v

echo ""
echo "==========================================="
echo "Buildando imagens do projeto..."
echo "==========================================="
docker compose build

echo ""
echo "==========================================="
echo "Subindo containers em segundo plano..."
echo "==========================================="
docker compose up -d

echo ""
echo "==========================================="
echo "Containers em execução:"
echo "==========================================="
docker ps

echo ""
echo "==========================================="
echo "⏳ Aguardando os serviços estabilizarem..."
echo "==========================================="
sleep 10

echo ""
echo "==========================================="
echo "Testando rotas da API Python com curl:"
echo "==========================================="

echo ""
echo "➡️ Teste: GET /ping"
curl -s http://localhost:8000/ping

echo ""
echo "➡️ Teste: GET /ping (API Python)"
curl -s http://localhost:8000/ping

echo ""
echo "➡️ Teste: GET /product (API Node.js -> API Python)"
curl -s http://localhost:3000/product

echo ""
echo "==========================================="
echo "Etapa de Teste - POST / PUT / DELETE - /product"
echo "==========================================="

# POST - Criar produto
echo ""
echo "➡️ Teste: POST /product"
RESPONSE=$(curl -s -X POST http://localhost:8000/product \
  -H "Content-Type: application/json" \
  -d '{"description": "Mouse Gamer", "category": "Periféricos", "price": 159.99}')
echo "Resposta: $RESPONSE"

# Extrair campos
ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)
DESCRIPTION=$(echo "$RESPONSE" | grep -o '"description":"[^"]*"' | cut -d':' -f2 | tr -d '"')
CATEGORY=$(echo "$RESPONSE" | grep -o '"category":"[^"]*"' | cut -d':' -f2 | tr -d '"')
PRICE=$(echo "$RESPONSE" | grep -o '"price":[0-9.]*' | cut -d':' -f2)

echo ""
echo "✔️ ID: $ID"
echo "✔️ Description: $DESCRIPTION"
echo "✔️ Category: $CATEGORY"
echo "✔️ Price: $PRICE"

# PUT - Atualizar produto
echo ""
echo "➡️ Teste: PUT /product/$ID"
UPDATE_RESPONSE=$(curl -s -X PUT http://localhost:8000/product/$ID \
  -H "Content-Type: application/json" \
  -d '{"description": "Mouse Gamer RGB", "category": "Acessórios", "price": 199.90}')
echo "Resposta: $UPDATE_RESPONSE"

# DELETE - Deletar produto
echo ""
echo "➡️ Teste: DELETE /product/$ID"
DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:8000/product/$ID)
echo "Resposta: $DELETE_RESPONSE"

echo ""
echo "==========================================="
echo "Testes concluídos. Acompanhe os logs abaixo:"
echo "==========================================="
docker compose logs -f
