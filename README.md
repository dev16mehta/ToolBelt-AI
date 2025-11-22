# ToolBelt-AI

## Target Users

- SMBs with limited knowledge
- DIY construction
- Individuals looking to start their own services business

## Plan

### Frontend

- Build a clean modern frontend with the following features:
  - Textfield where users can use natural language to describe the specification of the job they're looking to complete
  - Logo generation tool. Users can use natural language to describe the logo that they would like (call an API to generate )
    - Perhaps give the option for users to select pre configured styles that feed into the API call
  - Business name generation tool (same concept as above)
    (ultimately can add any tools here that new buisnesses might find useful)

### Backend

- Build a regression model based off the dataset to predict time and cost based off a host of inputs
- Use some agent (TBC) which is able to take the natural language textfield from the frontend (what specs the builder has) and extract the features that need to be fed into the regression model. Go from there

### Dataset

Here's the dataset[https://www.kaggle.com/datasets/sasakitetsuya/construction-estimation-data]
