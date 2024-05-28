import React from "react";
import Select from "react-select";
import { Noises } from "./noises";

// Define OptionType interface
interface OptionType {
  value: string;
  label: string;
}

// Define SelectProps interface
interface SelectProps {
  value: OptionType | null; // Allow null value
  onChange: (newValue: OptionType | null) => void;
  options: OptionType[]; // Define options prop
}

// Define MySelect component
const MySelect: React.FC<SelectProps> = ({ value, onChange, options }) => {
  return (
    <Select
      className="basic-single"
      classNamePrefix="select"
      value={value}
      onChange={onChange}
      options={options}
    />
  );
};

export default MySelect;
