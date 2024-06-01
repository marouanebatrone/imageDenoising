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

const noiseOptions: OptionType[] = [
  { value: 'Sel&&poivre', label: 'Sel&&poivre' },
  { value: 'Sel', label: 'Sel' },
  { value: 'Poivre', label: 'Poivre' },
  { value: 'Gaussian', label: 'Gaussian' },
];

const filterOptions: OptionType[] = [
  { value: 'filtre_gaussien', label: 'Filtre Gaussien' },
  { value: 'filtre_median', label: 'Filtre Médian' },
  { value: 'filtre_mean', label: 'Filtre Moyenne' },
  { value: 'filtre_min', label: 'Filtre Min' },
  { value: 'filtre_max', label: 'Filtre Max' },
];

interface FormInput {
  image: File[];
  noise: OptionType;
  filter: OptionType;
}

const MyForm = () => {
  const { control, handleSubmit } = useForm<FormInput>();
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [noisyImage, setNoisyImage] = useState<string | null>(null);
  const [filteredImage, setFilteredImage] = useState<string | null>(null);

  const onSubmit = async (data: FormInput) => {
    console.log("Form data:", data);
    const formData = new FormData();
    formData.append("original_image", data.image[0]);
    formData.append("selected_noise", data.noise.value);

    try {
      const createResponse = await axios.post('http://localhost:8000/api/images/', formData);
      console.log("Create response data:", createResponse.data);
      const imageId = createResponse.data.id;
      const originalImageUrl = createResponse.data.original_image;
      console.log("Original Image URL:", originalImageUrl);
      setOriginalImage(originalImageUrl);

      const noiseResponse = await axios.post(`http://localhost:8000/api/images/${imageId}/add_noise/`, { selected_noise: data.noise.value });
      console.log("Noise response data:", noiseResponse.data);
      const noisyImageUrl = noiseResponse.data.noisy_image_generated;
      setNoisyImage(noisyImageUrl);

      if (data.filter) {
        const filterResponse = await axios.post(`http://localhost:8000/api/images/${imageId}/apply_filter/`, { selected_filter: data.filter.value });
        console.log("Filter response data:", filterResponse.data);
        const filteredImageUrl = filterResponse.data.filtered_image_url;
        setFilteredImage(filteredImageUrl);
      }
    } catch (error) {
      console.error("Error:", error);
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
                options={noiseOptions}
              />
            )}
            control={control}
            name="noise"
          />
          <Button type="submit" variant="contained">
            Add
          </Button>

          {originalImage && (
            <div className="noisy-image-container">
              <p>Original image:</p>
              <img src={`http://localhost:8000${originalImage}`} alt="Original" />
            </div>
          )}

          {noisyImage && (
            <div className="noisy-image-container">
              <p>Noisy image generated:</p>
              <img src={`http://localhost:8000${noisyImage}`} alt="Noisy" />
            </div>
          )}

          {filteredImage && (
            <div className="noisy-image-container">
              <p>Filtered image:</p>
              <img src={`http://localhost:8000${filteredImage}`} alt="Filtered" />
            </div>
          )}

          <div>
            <h3>Add a filter to the image</h3>
            <Controller
              render={({ field: { value, onChange } }) => (
                <MySelect
                  value={value}
                  onChange={onChange}
                  options={filterOptions}
                />
              )}
              control={control}
              name="filter"
            />
            <Button type="submit" variant="contained">
              Denoise
            </Button>
          </div>

        </div>
      </Box>
    </Box>
  );
};

export default MyForm;
