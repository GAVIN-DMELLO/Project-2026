```mermaid
graph LR
    %% Request Path
    A[Frontend] -- "HTTP Request" --> C

    subgraph B [Backend API]
        direction LR
        C[Middleware] --> D
        
        subgraph D [Router]
            direction TB
            D1[Decorator] --> D2[Route Handler]
        end
    end

    D2 --> E

    subgraph E [Service Layer]
        F[Backend Logic .py]
    end

    %% Response Path
    F --> D2
    D2 -- "HTTP Response" --> A

    G[Environment Variables] -- Fetching Environment Variables --> E

    F -- "Send Prompt/Data" --> H[Gemini API]
    H -- "Return Summary/Response" --> F

    %% Styling
    style A fill:#2d3436,stroke:#00cec9,color:#fff
    style B fill:#2d3436,stroke:#636e72,color:#fff
    style E fill:#2d3436,stroke:#636e72,color:#fff
    style F fill:#0984e3,stroke:#74b9ff,color:#fff
    style G fill:#636e72,stroke:#dfe6e9,color:#fff
    style H fill:#6c5ce7,stroke:#a29bfe,color:#fff
    style D1 fill:#555,stroke:#fff,color:#fff
    style D2 fill:#555,stroke:#fff,color:#fff
