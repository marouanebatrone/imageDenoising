import { Box, Button } from "@mui/material";
import { Controller, useForm } from "react-hook-form";
import FileUpload from "react-material-file-upload";
import MySelect from "./Select";
import "../styles.css";
import axios from "axios";
import { useState } from "react";

interface OptionType {
  value: string;
  label: string;
}

const options: OptionType[] = [
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
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [noisyImage, setNoisyImage] = useState<string | null>(null);

  const onSubmit = async (data: FormInput) => {
    console.log("Form data:", data); // Log form data for debugging
    const formData = new FormData();
    formData.append("original_image", data.image[0]);
    formData.append("selected_noise", data.noise.value);

    try {
      const createResponse = await axios.post('http://localhost:8000/api/images/', formData);
      console.log("Create response data:", createResponse.data); // Log create response data for debugging
      const imageId = createResponse.data.id;
      const originalImageUrl = createResponse.data.original_image; // Get the original image URL from the response
      console.log("Original Image URL:", originalImageUrl); // Log the original image URL
      setOriginalImage(originalImageUrl); // Set the original image URL state

      const noiseResponse = await axios.post(`http://localhost:8000/api/images/${imageId}/add_noise/`, { selected_noise: data.noise.value });
      console.log("Noise response data:", noiseResponse.data); // Log noise response data for debugging
      const imageUrl = noiseResponse.data.noisy_image_generated;
      setNoisyImage(imageUrl);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        // Handle Axios error
        console.error("There was an error uploading the image!", error.message);
        console.log("Error response:", error.response); // Log error response for debugging
      } else {
        // Handle other errors
        console.error("An unexpected error occurred", error);
      }
    }
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

          {originalImage && (
            <div className="image-container">
              <p>Original image:</p>
              <img src={`http://localhost:8000${originalImage}`} alt="Original" />
            </div>
          )}

          {noisyImage && (
            <div className="image-container">
              <p>Noisy image generated:</p>
              <img src={`http://localhost:8000${noisyImage}`} alt="Noisy" />
              <Button type="submit" variant="contained">
                Denoise
              </Button>
            </div>
          )}
        </div>
      </Box>
    </Box>
  );
};

export default MyForm;
