import { ComponentPreview, Previews } from "@react-buddy/ide-toolbox";
import { PaletteTree } from "./palette";
import { ButtonLightDark, Header } from "../components/nav";
import HomePage from "../pages/HomePage/HomePage.tsx";
import { LoginPage } from "../pages/auth/LoginPage";

const ComponentPreviews = () => {
  return (
    <Previews palette={<PaletteTree />}>
      <ComponentPreview path="/ButtonLightDark">
        <ButtonLightDark />
      </ComponentPreview>
      <ComponentPreview path="/Header">
        <Header />
      </ComponentPreview>
      <ComponentPreview path="/HomePage">
        <HomePage />
      </ComponentPreview>
      <ComponentPreview path="/LoginPage">
        <LoginPage />
      </ComponentPreview>
    </Previews>
  );
};

export default ComponentPreviews;
