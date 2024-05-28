import { Box, Button } from "@mui/material";
import { Controller, useForm } from "react-hook-form";
import FileUpload from "react-material-file-upload";
import MySelect from "./Select"; // Import MySelect component
import "../styles.css";
import axios from "axios";
import { useState } from "react";


interface OptionType {
  value: string;
  label: string;
}


const options: OptionType[] = [
  { value: 'Laplacien', label: 'Laplacien' },
  { value: 'Sel&&poivre', label: 'Sel&&poivre' },
  { value: 'Sel', label: 'Sel' },
  { value: 'Poivre', label: 'Poivre' },
];


interface FormInput {
  image: File[];
  noise: OptionType; 
}

const MyForm = () => {
  const { control, handleSubmit } = useForm<FormInput>();
  const [noisyImage, setNoisyImage] = useState<string | null>(null);

  const onSubmit = (data: FormInput) => {
    const formData = new FormData();
    formData.append("original_image", data.image[0]);
    formData.append("selected_noise", data.noise.value);

    axios.post('http://localhost:8000/image_processing/api/images/', formData)
      .then(response => {
        setNoisyImage(response.data.original_image);
      })
      .catch(error => {
        console.error("There was an error uploading the image!", error);
      });
  };

  return (
    <Box
      component="form"
      sx={{ paddingTop: 1 }}
      noValidate
      autoComplete="off"
      onSubmit={handleSubmit(onSubmit)}
    >
      <Box
        sx={{
          mt: 2,
          textAlign: "center",
          fontFamily: "Montserrat, sans-serif",
        }}
      >
        <div className="noise-section">
          <Controller
            render={({ field: { value, onChange } }) => (
              <FileUpload
                value={value}
                onChange={onChange}
                multiple={false}
                title="Click to select or drag and drop a image."
                buttonText="Select image"
                maxSize={7340032}
              />
            )}
            control={control}
            name="image"
          />
          <h3>Add a noise to the image</h3>
          <Controller
            render={({ field: { value, onChange } }) => (
              <MySelect
                value={value}
                onChange={onChange}
                options={options} 
              />
            )}
            control={control}
            name="noise"
          />
          <Button type="submit" variant="contained">
            Add
          </Button>

          {noisyImage && (
            <div>
              <p>Noisy image generated:</p>
              <img src={`http://localhost:8000${noisyImage}`} alt="Noisy" />
            </div>
          )}
        </div>
      </Box>
    </Box>
  );
};

export default MyForm;
