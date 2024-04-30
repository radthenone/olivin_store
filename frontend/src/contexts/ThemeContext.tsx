import { createContext } from "react";
import { ThemeContextProps } from "./ThemeContextInterface.tsx";

export const ThemeContext = createContext<ThemeContextProps | undefined>(
  undefined,
);
