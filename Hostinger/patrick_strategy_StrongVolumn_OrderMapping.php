<?php
$servername = "?;
$username = "?";
$password = "?";
$dbname = "?";

// Create a connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data from the database
$sql = "SELECT * FROM patrick_strategy_StrongVolumn_OrderMapping";
$result = $conn->query($sql);

// Close the connection
$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Sortable Table</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            text-align: left;
            padding: 8px;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.1/js/jquery.dataTables.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.11.1/css/jquery.dataTables.min.css">
    <script>
        $(document).ready(function() {
            $('#myTable').DataTable();
        });
    </script>
</head>
<body>
    <table id="myTable">
        <thead>
            <tr>
                <th>id</th>
                <th>symbol</th>
                <th>quality</th>
                <th>createDateTime</th>
                <th>keyPosition</th>
                <th>openPosition</th>
                <th>stopProfitsPosition</th>
                <th>stopLostPosition</th>
                <th>offsetPosition</th>
                <th>status</th>
                <!-- Add more columns here -->
            </tr>
        </thead>
        <tbody>
            <?php
            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>" . $row['id'] . "</td>";
                    echo "<td>" . $row['symbol'] . "</td>";
                    echo "<td>" . $row['quality'] . "</td>";
                    echo "<td>" . $row['createDateTime'] . "</td>";
                    echo "<td>" . $row['keyPosition'] . "</td>";
                    echo "<td>" . $row['openPosition'] . "</td>";
                    echo "<td>" . $row['stopProfitsPosition'] . "</td>";
                    echo "<td>" . $row['stopLostPosition'] . "</td>";
                    echo "<td>" . $row['offsetPosition'] . "</td>";
                    echo "<td>" . $row['status'] . "</td>";
                    // Add more columns here
                    echo "</tr>";
                }
            }
            ?>
        </tbody>
    </table>
</body>
</html>
