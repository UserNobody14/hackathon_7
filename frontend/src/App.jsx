import { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import NewspaperOutlinedIcon from "@mui/icons-material/NewspaperOutlined";
import EmojiNatureOutlinedIcon from "@mui/icons-material/EmojiNatureOutlined";
import LoyaltyOutlinedIcon from "@mui/icons-material/LoyaltyOutlined";
import CircularProgress from "@mui/material/CircularProgress";
import { useMutation } from "@tanstack/react-query";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  // Mutations
  const mutation = useMutation({
    queryKey: ["generate_video", { text: input }],
    onSettled: () => {
      setLoading(false);
    },
    mutationFn: async (input) => {
      // Make a request to the server
      const response = await fetch("/generate_video/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
    onSuccess: () => {
      console.log("Success");
      // Invalidate and refetch
      //queryClient.invalidateQueries({ queryKey: ['todos'] })
      setSubmitted(true);
    },
  });

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   setLoading(true);
  //   setTimeout(() => {
  //     setSubmitted(true);
  //     setLoading(false);
  //   }, 5000); // Simulate loading
  // };

  const suggestedSubmit = (i) => {
    setLoading(true);
    mutation.mutate(i);
    // setInput(i);
    // setTimeout(() => {
    //   setSubmitted(true);
    //   setLoading(false);
    // }, 5000); // Simulate loading
  };

  return (
    <>
      {mutation.isError && (
        <Typography variant="h3" color="red">
          An error occurred: {mutation.error.message}
        </Typography>
      )}
      {/* {
      mutation.isSuccess && <Typography variant='h3' color='green'>Success!</Typography>
    } */}
      {loading && <Typography variant="h3">Loading...</Typography>}
      {!submitted && !loading && (
        <div>
          <div>
            <img
              src="/logo.png"
              alt="Logo"
              style={{ width: "600px", height: "auto" }}
            />
          </div>
          <Typography variant="h2" fontWeight="bold" color="black">
            What do you want to watch today?
          </Typography>
          <form
            onSubmit={() => {
              setLoading(true);
              mutation.mutate(input);
              //setLoading(true);
            }}
            style={{
              display: "flex",
              flexDirection: "row",
              alignItems: "center",
            }}
          >
            <TextField
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter a movie or show"
              variant="outlined"
              fullWidth
              margin="normal"
              sx={{
                "& .MuiOutlinedInput-root": {
                  "&.Mui-focused fieldset": {
                    borderColor: "lightgrey", // Change this to the color you want
                  },
                },
              }}
            />
            <Button
              type="submit"
              variant="contained"
              sx={{
                textTransform: "none",
                ml: 1,
                bgcolor: "grey",
                "&:hover": {
                  backgroundColor: "lightgrey",
                },
              }}
            >
              Enter
            </Button>
          </form>
          <Stack
            direction="row"
            spacing={1}
            justifyContent="center"
            sx={{ mx: "auto" }}
          >
            <Button
              variant="text"
              startIcon={<NewspaperOutlinedIcon />}
              sx={{
                textTransform: "none",
                color: "grey",
                "&:hover": {
                  backgroundColor: "lightgrey",
                },
              }}
              onClick={() => suggestedSubmit("show me the latest news")}
            >
              Show me the latest geopolitical news
            </Button>
            <Button
              variant="text"
              startIcon={<EmojiNatureOutlinedIcon />}
              sx={{
                textTransform: "none",
                color: "grey",
                "&:hover": {
                  backgroundColor: "lightgrey",
                },
              }}
              onClick={() => suggestedSubmit("tell me about the Amazon")}
            >
              Tell me about the Amazon rain forrest
            </Button>
            <Button
              variant="text"
              startIcon={<LoyaltyOutlinedIcon />}
              sx={{
                textTransform: "none",
                color: "grey",
                "&:hover": {
                  backgroundColor: "lightgrey",
                },
              }}
              onClick={() => suggestedSubmit("make me an ad")}
            >
              Generate an coke advertisement
            </Button>
          </Stack>
        </div>
      )}
      {submitted && !loading && (
        <Stack alignItems="center">
          <Typography fontWeight="bold">Here&apos;s your short!</Typography>
          <video width="400" controls style={{ borderRadius: "15px" }}>
            <source src={mutation.data?.video_url} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <Button
            variant="contained"
            sx={{
              textTransform: "none",
              mt: 1,
              bgcolor: "grey",
              "&:hover": {
                backgroundColor: "lightgrey",
              },
            }}
            onClick={() => setSubmitted(false)}
          >
            Make Another
          </Button>
        </Stack>
      )}
      {loading && (
        <Stack alignItems="center" spacing={1}>
          <Stack alignItems="center">
            <Typography fontWeight="bold" variant="h3">
              Generating a short for:{" "}
            </Typography>
            <Typography variant="h3">{input}</Typography>
          </Stack>
          <CircularProgress sx={{ color: "grey" }} />
        </Stack>
      )}
    </>
  );
}

export default App;
