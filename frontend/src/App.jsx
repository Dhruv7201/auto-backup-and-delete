import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import StoreCodeDetails from "./pages/StoreCodeDetails";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/store-code/:storeCode" element={<StoreCodeDetails />} />
    </Routes>
  );
}

export default App;
