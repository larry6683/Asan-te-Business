# ⚛️ ASANTe Registration Client

React frontend application for the ASANTe Platform registration flow with Material-UI, AWS Cognito authentication, and gRPC-Web communication.

---

## 🎯 Overview

The registration client is a modern React application that provides:
- **Multi-step registration flow** (6 steps: signup → verification → first login → causes → size → entity info)
- **AWS Cognito authentication** for secure user management
- **gRPC-Web communication** with backend microservices
- **Analytics tracking** for user journey monitoring
- **Responsive design** across mobile, tablet, and desktop
- **Material-UI components** for professional appearance

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 16+ with npm
- **Backend services** running (see main README)
- **Envoy proxy** running on port 8080
- **AWS Cognito** user pool configured

### 1. Install Dependencies

```bash
cd registration-flow-client
npm install
```

### 2. Configure Environment

Create `.env.local` file:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your AWS Cognito credentials:

```env
# AWS Cognito Configuration
REACT_APP_USER_POOL_ID=your_user_pool_id
REACT_APP_CLIENT_ID=your_client_id
REACT_APP_REGION=us-east-2

# gRPC Endpoint
REACT_APP_GRPC_ENDPOINT=http://localhost:8080
```

> ⚠️ **Never commit `.env.local`** - It's in `.gitignore` for security.

### 3. Generate Protobuf Files

```bash
# Make script executable (first time only)
chmod +x scripts/generate-proto.sh

# Generate gRPC-Web client code
./scripts/generate-proto.sh
```

**This creates:**
- `src/proto/user/*_pb.js` - User service client
- `src/proto/business/*_pb.js` - Business service client
- `src/proto/beneficiary/*_pb.js` - Beneficiary service client
- `src/proto/analytics/*_pb.js` - Analytics service client

### 4. Start Development Server

```bash
npm start
```

**Application opens at:** `http://localhost:3000`

---

## 📦 Tech Stack

### Core
- **React** 18.3.1 - UI library
- **React Router** 6.23.1 - Navigation
- **Redux Toolkit** 2.2.5 - State management

### UI Framework
- **Material-UI** 5.15.19 - Component library
- **@emotion** - CSS-in-JS styling
- **Material Icons** - Icon set

### Authentication
- **amazon-cognito-identity-js** 6.3.12 - AWS Cognito SDK

### gRPC Communication
- **grpc-web** 2.0.2 - gRPC for browsers
- **google-protobuf** 4.0.0 - Protocol buffers

### Utilities
- **validator** 13.12.0 - Input validation
- **react-transition-group** - Animations

---

## 📁 Project Structure

```
registration-flow-client/
├── public/                     # Static assets
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── api/                    # gRPC service clients
│   │   ├── grpcService.js      # Base gRPC setup
│   │   ├── userApiService.js   # User service wrapper
│   │   ├── businessApiService.js
│   │   ├── beneficiaryApiService.js
│   │   └── analyticsService.js # Analytics tracking
│   │
│   ├── components/             # React components
│   │   ├── Login.js            # Login page
│   │   ├── SignUp.js           # Signup page
│   │   ├── VerificationComponent.js
│   │   ├── CausesComponent.js  # Cause selection
│   │   ├── SizeOptionSelection.js
│   │   ├── CombinedForm.js     # Final registration
│   │   ├── HomePage.js         # Post-registration
│   │   ├── AnalyticsDashboard.js
│   │   └── *.module.css        # Component styles
│   │
│   ├── user-auth/              # Cognito authentication
│   │   ├── asanteUsersUserPool.js
│   │   └── authenticateUser.js
│   │
│   ├── proto/                  # Generated gRPC files
│   │   ├── user/
│   │   ├── business/
│   │   ├── beneficiary/
│   │   ├── analytics/
│   │   └── error/
│   │
│   ├── redux/                  # Redux state management
│   │   ├── store.js
│   │   ├── userSlice.js
│   │   ├── emailSlice.js
│   │   └── selectedOptionSlice.js
│   │
│   ├── cookies/                # Cookie management
│   │   └── cookieFactory.js
│   │
│   ├── types/                  # Type definitions
│   │   └── userType.js
│   │
│   ├── web-data/               # Constants
│   │   └── redirectUrls.js
│   │
│   ├── assets/                 # Images and media
│   ├── App.js                  # Main app component
│   ├── App.css                 # Global styles
│   └── index.js                # Entry point
│
├── scripts/
│   └── generate-proto.sh       # Proto generation script
│
├── .env.local                  # Local config (not in git)
├── .env.example                # Config template
├── .gitignore                  # Git ignore rules
├── package.json                # Dependencies
└── README.md                   # This file
```

---

## 🔧 Development

### Available Scripts

#### `npm start`
Runs the app in development mode at `http://localhost:3000`

- Hot reload on file changes
- Lint errors in console
- Development source maps

#### `npm test`
Launches test runner in interactive watch mode

```bash
npm test
```

#### `npm run build`
Creates production build in `build/` folder

```bash
npm run build
```

**Production build includes:**
- Minified code
- Optimized assets
- Hashed filenames for caching
- Source maps (optional)

#### Code Formatting

**Format all files with Prettier:**
```bash
npx prettier . --write
```

> ⚠️ **Important:** Always run Prettier before committing code and creating Pull Requests!

### VSCode Setup

**Recommended Extensions:**
- **Prettier** - Code formatter
- **ESLint** - Linting
- **ES7+ React/Redux** - Snippets

**Settings:**
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

---

## 🎨 Registration Flow

### Step 1: Welcome / User Type Selection
**Route:** `/`  
**Component:** `RegisteringAsComponent.js`  
- User selects Business or Non-Profit
- Sets user type in Redux store

### Step 2: Sign Up
**Route:** `/register/signup`  
**Component:** `SignUp.js`  
- Email and password input
- AWS Cognito user creation
- Email verification code sent

### Step 3: Verification
**Route:** `/register/verification`  
**Component:** `VerificationComponent.js`  
- Enter verification code
- Confirm Cognito account
- Track verification attempts

### Step 4: First Login
**Route:** `/` (redirected after verification)  
**Component:** `Login.js`  
- User logs in with credentials
- Session cookie created
- Redirects based on registration status

### Step 5: Cause Selection
**Route:** `/register/causes`  
**Component:** `CausesComponent.js`  
- **Business:** Select 3+ causes
- **Non-Profit:** Select 1 primary + up to 2 supporting causes

### Step 6: Size Selection
**Route:** `/register/sizeoptionselection`  
**Component:** `SizeOptionSelection.js`  
- Select organization size (Small / Medium / Large)

### Step 7: Entity Information
**Route:** `/register/registrationform`  
**Component:** `CombinedForm.js` (renamed to RegistrationForm)  
- Organization name, location, contact info
- Tax ID, description
- Social media (optional)
- Final submission

### Step 8: Home
**Route:** `/home`  
**Component:** `HomePage.js`  
- Post-registration dashboard
- Welcome message

---

## 🔐 Authentication

### AWS Cognito Integration

**User Pool Configuration:**
```javascript
// src/user-auth/asanteUsersUserPool.js
const AsanteUsersUserPoolData = {
  UserPoolId: process.env.REACT_APP_USER_POOL_ID,
  ClientId: process.env.REACT_APP_CLIENT_ID
};
```

**Authentication Flow:**
1. User enters email/password
2. Cognito validates credentials
3. JWT tokens issued
4. Tokens stored in cookies
5. Backend validates tokens via Cognito

**Cookie Management:**
```javascript
// Session cookie
document.cookie = `asanteApp=${sessionId}; path=/; max-age=86400`;

// Retrieve session
const sessionCookie = document.cookie
  .split('; ')
  .find(row => row.startsWith('asanteApp='));
```

---

## 📡 gRPC Communication

### Service Clients

**User Service:**
```javascript
import { UserApiService } from './api/userApiService';

// Create user
const response = await UserApiService.createUser(email, userType, mailingList);

// Get user by email
const user = await UserApiService.getUserByEmail(email);
```

**Analytics Service:**
```javascript
import { analyticsService } from './api/analyticsService';

// Track registration step
await analyticsService.trackStep(stepCode, appUserId, sessionId);

// Complete step
await analyticsService.completeStep(interactionId);

// Get dashboard KPIs
const kpis = await analyticsService.getDashboardKPIs();
```

**Business Service:**
```javascript
import { BusinessApiService } from './api/businessApiService';

// Create business
const business = await BusinessApiService.createBusiness({
  businessName,
  email,
  locationCity,
  locationState,
  // ...
});
```

### gRPC-Web Setup

**Endpoint Configuration:**
```javascript
// src/api/grpcService.js
const GRPC_ENDPOINT = process.env.REACT_APP_GRPC_ENDPOINT || 'http://localhost:8080';
```

**Making Requests:**
```javascript
const client = new UserServiceClient(GRPC_ENDPOINT);
const request = new GetUserRequest();
request.setEmail(email);

client.getUser(request, {}, (err, response) => {
  if (err) {
    console.error('Error:', err);
  } else {
    const user = response.getUser();
    // Handle user data
  }
});
```

---

## 🎯 State Management

### Redux Store

**Slices:**
- `userSlice` - User data (id, email, type)
- `emailSlice` - Email for verification flow
- `selectedOptionSlice` - User type selection (Business/Non-Profit)

**Usage:**
```javascript
import { useSelector, useDispatch } from 'react-redux';
import { setUser } from './redux/userSlice';

// Get state
const user = useSelector(state => state.user);

// Update state
const dispatch = useDispatch();
dispatch(setUser({ id, email, userType }));
```

---

## 🧪 Testing

### Run Tests

```bash
npm test
```

### Test Coverage

```bash
npm test -- --coverage
```

### E2E Testing Flow

1. Navigate to `http://localhost:3000`
2. Click "Create Account"
3. Select Business or Non-Profit
4. Enter email: `test+user1@gmail.com`
5. Enter password: `TestPassword123!`
6. Check email for verification code
7. Enter code and verify
8. Log in with credentials
9. Complete registration steps
10. Verify redirect to `/home`

### Testing with Email Aliases

Use Gmail's `+` feature to create multiple test accounts:
```
yourname+business1@gmail.com
yourname+business2@gmail.com
yourname+nonprofit1@gmail.com
```

All emails arrive at `yourname@gmail.com`.

---

## 🐛 Troubleshooting

### "Cannot find module" errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### gRPC connection errors

**Check Envoy proxy is running:**
```bash
curl http://localhost:8080
# Should return some response (not refused)

# Check Envoy logs
docker logs envoy_proxy
```

**Check backend services:**
```bash
# Verify services are running
lsof -i :50051  # User Service
lsof -i :50052  # Business Service
lsof -i :50053  # Beneficiary Service
lsof -i :50054  # Analytics Service
```

### Protobuf errors

```bash
# Regenerate proto files
cd scripts
./generate-proto.sh

# Verify generated files exist
ls -la ../src/proto/user/
ls -la ../src/proto/business/
ls -la ../src/proto/analytics/
```

### AWS Cognito errors

**Check environment variables:**
```bash
cat .env.local | grep REACT_APP
```

**Verify Cognito configuration:**
1. Check User Pool ID is correct
2. Check Client ID is correct
3. Verify region matches
4. Ensure app client has no secret

### Cookie/Session issues

**Check cookies in browser:**
1. Open DevTools (F12)
2. Application tab → Cookies
3. Verify `asanteApp` cookie exists
4. Check cookie value is a valid UUID

**Clear cookies:**
```javascript
// In browser console
document.cookie = "asanteApp=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
```

---

## 🎨 Styling

### Material-UI Theming

**Custom theme:**
```javascript
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#dc004e' }
  }
});
```

### CSS Modules

Component-specific styles use CSS Modules:
```javascript
import styles from './Login.module.css';

<div className={styles.container}>
  <h1 className={styles.title}>Login</h1>
</div>
```

### Global Styles

Global styles in `App.css`:
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
}
```

---

## 📚 Additional Resources

- **React Documentation:** https://reactjs.org/
- **Material-UI:** https://mui.com/
- **gRPC-Web:** https://github.com/grpc/grpc-web
- **AWS Cognito:** https://docs.aws.amazon.com/cognito/
- **Redux Toolkit:** https://redux-toolkit.js.org/

---

## 🤝 Contributing

### Code Style

- Use functional components with hooks
- Follow Prettier formatting (run before commit)
- Use meaningful variable names
- Add comments for complex logic
- Keep components focused and small

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test locally
3. Run Prettier: `npx prettier . --write`
4. Commit with clear message
5. Push and create Pull Request
6. Ensure all checks pass

---

## 📄 License

This project is proprietary and confidential.

---

<div align="center">

**[⬆ Back to Top](#️-asante-registration-client)**

---

**ASANTe Registration Client**

*Modern • Secure • Responsive*

</div>