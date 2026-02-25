Add-Type -Path "C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll"

$connStr = "Data Source=localhost:59964;Initial Catalog=a6920105-2054-4385-8c6f-cb9fb18bca1a"
$conn = New-Object Microsoft.PowerBI.AdomdClient.AdomdConnection($connStr)

try {
    $conn.Open()
    Write-Host "Conexion exitosa!"
    Write-Host "Estado: $($conn.State)"
    $conn.Close()
} catch {
    Write-Host "Error: $_"
}
