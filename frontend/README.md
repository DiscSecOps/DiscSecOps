
### Frontend Tech Stack

- **React 19** with Vite
- **React Router DOM** v6
- **Axios** for HTTP requests
- **Vitest** + Testing Library (unit/integration)
- **Playwright BDD** (E2E with Gherkin)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev  # [http://localhost:3000]
```

### Unit/Integration Tests

```bash
cd frontend
npm test  # Vitest watch mode
npm run test:run  # Single run
```

### E2E Tests (Playwright BDD)

npm run test:e2e  # Runs all .feature files
npm run test:e2e:ui  # Interactive UI

frontend/                    # React + Vite
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   ├── services/
│   │   └── App.jsx
│   ├── tests
│   │   ├── unit/              # Vitest tests
│   │   └── e2e/               # Playwright BDD tests
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── vitest.config.js
│   └── playwright.config.js

### API:

http://localhost:3000/login
http://localhost:3000/register

