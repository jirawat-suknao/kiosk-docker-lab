## System Architecture Diagram

```mermaid
graph LR
    Client([Web Browser]) -->|HTTP Port 5000| WebApp(Kiosk Web Dashboard)
    WebApp -->|Port 6379| Database[(Redis Database)]
    
    classDef container fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    class WebApp,Database container;
