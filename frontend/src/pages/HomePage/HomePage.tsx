const HomePage = () => {
  return (
    <div>
      <h1>Home Page</h1>
      <p>{process.env.API_BACKEND_URL}</p>
    </div>
  );
};

export default HomePage;
