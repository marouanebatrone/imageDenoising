// App.tsx

import "./styles.css";
import MyForm from "./components/my-from";

export default function App() {
  return (
    <div className="container">
      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        Image Denoising
      </h1>

      {/* Upload Form Section */}
      <div className="form-section">
        <MyForm />
      </div>
    </div>
  );
}
