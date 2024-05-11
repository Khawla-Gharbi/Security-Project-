<?php
    $servername = "localhost";
    $dbname = "user_credentials";

    // Create connection
    $conn = new mysqli($servername, "", "", $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Check if form is submitted
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Hash the password
        $hashed_password = password_hash($_POST['password'], PASSWORD_DEFAULT);

        // Prepare and bind
        $stmt = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
        $stmt->bind_param("ss", $_POST['username'], $hashed_password);

        // Execute and check for errors
        if ($stmt->execute()) {
            echo "New user created successfully";
        } else {
            echo "Error: " . $stmt->error;
        }

        // Close statement and connection
        $stmt->close();
    }

    $conn->close();
?>
