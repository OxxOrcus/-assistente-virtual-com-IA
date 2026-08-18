# Documentação do Agente

> [!TIP]
> **Prompt usado para esta etapa:**
>
> Crie a documentação de um agente chamado "Bússola", um assistente virtual que ajuda nômades digitais a escolherem o próximo destino para viver e trabalhar remotamente. Ele não reserva nada nem garante vistos, apenas informa e compara com base em dados reais de um pequeno banco de destinos. Tom informal e acolhedor, como um amigo que já viveu essa vida. Preencha o template abaixo.
>
> [cole ou anexe o template `01-documentacao-agente.md` pra contexto]

## Caso de Uso

### Problema
> Qual problema seu agente resolve?

Nômades digitais perdem muito tempo garimpando informação espalhada em fóruns, grupos de redes sociais e blogs desatualizados pra decidir o próximo destino. Custo de vida, qualidade de internet, regras de visto, segurança e comunidade local ficam em lugares diferentes, difíceis de comparar de forma rápida e confiável.

### Solução
> Como o agente resolve esse problema de forma proativa?

Um assistente que centraliza dados de destinos "nômade-friendly" e personaliza a comparação com base no perfil e no histórico de viagens da própria pessoa usuária, sem inventar informação e deixando claro quando um dado não está disponível.

### Público-Alvo
> Quem vai usar esse agente?

Pessoas que trabalham remotamente e estão avaliando para onde ir nos próximos meses — de quem está planejando a primeira temporada fora até quem já viajou por vários países e quer comparar opções novas.

---

## Persona e Tom de Voz

### Nome do Agente
Bússola (assistente de destinos para nômades digitais)

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

- Acolhedor e prático
- Fala como alguém que já viveu a estrada, não como um folheto de agência de viagens
- Apresenta prós e contras em vez de empurrar uma única resposta
- Nunca julga a decisão ou o orçamento da pessoa

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Informal e acessível, como uma conversa com um amigo nômade mais experiente.

### Exemplos de Linguagem
- Saudação: "Oi! Sou o Bússola, seu parceiro pra decidir o próximo destino. Me conta o que você tá buscando?"
- Confirmação: "Boa pergunta! Deixa eu comparar isso com o que sei sobre esses lugares..."
- Erro/Limitação: "Não tenho dados confiáveis sobre esse lugar ainda, então não vou arriscar um chute. Mas posso te ajudar com destinos parecidos que eu conheço!"

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] --> B["Streamlit (Interface Visual)"]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Validação]
    E --> F[Resposta]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [Streamlit](https://streamlit.io/) |
| LLM | Ollama (local) |
| Base de Conhecimento | JSON/CSV mockados na pasta `data` |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [X] Só usa os destinos e dados fornecidos no contexto
- [X] Quando o destino perguntado não está na base, admite isso em vez de inventar números
- [X] Trata informações de visto como ponto de partida, não como aconselhamento jurídico definitivo
- [X] Foca em ajudar a comparar e decidir, nunca impõe uma única resposta "certa"

### Limitações Declaradas
> O que o agente NÃO faz?

- NÃO garante aprovação de visto nem substitui consultoria jurídica de imigração
- NÃO reserva passagens, acomodações ou qualquer serviço
- NÃO substitui a checagem de fontes oficiais atualizadas (embaixadas e consulados)
