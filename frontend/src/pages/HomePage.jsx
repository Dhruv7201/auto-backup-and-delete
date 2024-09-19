import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { get } from "../api/api";
import {
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  TextField,
  TablePagination,
  TableSortLabel,
  Button,
  Tab,
} from "@mui/material";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import exportToExcel from "../utils/convertToExcel";
import "./HomePage.css";

const formateDate = (date) => {
  const dateObj = new Date(date);
  const year = dateObj.getFullYear();
  const month = dateObj.getMonth() + 1;
  const day = dateObj.getDate();
  return `${month}/${day}/${year}`;
};

const HomePage = () => {
  const [data, setData] = useState(null);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("storeCode");
  const [selectedFlag, setSelectedFlag] = useState("All");

  useEffect(() => {
    get("/")
      .then((res) => {
        setData(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
  };

  const handleFlagChange = (event) => {
    setSelectedFlag(event.target.value);
  };

  const filteredData = data
    ? Object.entries(data)
        .filter(([storeCode, storeData]) =>
          storeCode.toLowerCase().includes(search.toLowerCase())
        )
        .map(([storeCode, storeData]) => ({
          storeCode,
          ...storeData,
        }))
    : [];

  const filteredDataByFlag = selectedFlag
    ? filteredData.filter(
        (item) => item.flag === selectedFlag || selectedFlag === "All"
      )
    : filteredData;

  const exportData = () => {
    const dataToExport = filteredDataByFlag.map((item) => ({
      storeCode: item.storeCode,
      total_bucket_files: item.total_bucket_files,
      total_size: item.total_size,
      last_backup_date: item.last_backup_date,
      last_deleted_date: item.last_deleted_date,
      flag: item.flag,
    }));
    // save excel file in date month year format
    exportToExcel(dataToExport, `store-code-data-${formateDate(new Date())}`);
  };

  return (
    <>
      {data ? (
        <div>
          <h1>Home Page</h1>
          <div className="search-and-export-container">
            <div className="search-container">
              <TextField
                label="Search"
                value={search}
                onChange={handleSearchChange}
                style={{ margin: "10px" }}
              />
              <Select
                value={selectedFlag}
                onChange={handleFlagChange}
                style={{ margin: "10px" }}
              >
                <MenuItem value="All">All</MenuItem>
                <MenuItem value="success">Success</MenuItem>
                <MenuItem value="warning">Warning</MenuItem>
                <MenuItem value="danger">Danger</MenuItem>
              </Select>
            </div>
            <Button variant="contained" onClick={exportData}>
              Export to Excel
            </Button>
          </div>
          <div className="table-container">
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "storeCode"}
                        direction={orderBy === "storeCode" ? order : "asc"}
                        onClick={() => handleRequestSort("storeCode")}
                      >
                        Store Code
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "total_size"}
                        direction={orderBy === "total_size" ? order : "asc"}
                        onClick={() => handleRequestSort("total_size")}
                      >
                        Total Size
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "total_bucket_files"}
                        direction={
                          orderBy === "total_bucket_files" ? order : "asc"
                        }
                        onClick={() => handleRequestSort("total_bucket_files")}
                      >
                        Total Bucket Files
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "last_backup_date"}
                        direction={
                          orderBy === "last_backup_date" ? order : "asc"
                        }
                        onClick={() => handleRequestSort("last_backup_date")}
                      >
                        Last Backup Date
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "last_backup_time"}
                        direction={
                          orderBy === "last_backup_time" ? order : "asc"
                        }
                        onClick={() => handleRequestSort("last_backup_time")}
                      >
                        Last Backup Time
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "last_delete_date"}
                        direction={
                          orderBy === "last_delete_date" ? order : "asc"
                        }
                        onClick={() => handleRequestSort("last_delete_date")}
                      >
                        Last Delete Date
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "flag"}
                        direction={orderBy === "flag" ? order : "asc"}
                        onClick={() => handleRequestSort("flag")}
                      >
                        Flag
                      </TableSortLabel>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredDataByFlag
                    .sort((a, b) => {
                      const valueA =
                        typeof a[orderBy] === "number"
                          ? a[orderBy]
                          : String(a[orderBy] || "");
                      const valueB =
                        typeof b[orderBy] === "number"
                          ? b[orderBy]
                          : String(b[orderBy] || "");

                      if (order === "asc") {
                        return valueA < valueB ? -1 : valueA > valueB ? 1 : 0;
                      } else {
                        return valueA > valueB ? -1 : valueA < valueB ? 1 : 0;
                      }
                    })
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((item, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Link
                            className="styled-link"
                            to={`/store-code/${item.storeCode}`}
                          >
                            {item.storeCode}
                          </Link>
                        </TableCell>
                        <TableCell>{`${item.total_size} GB`}</TableCell>
                        <TableCell>{item.total_bucket_files}</TableCell>
                        <TableCell>{item.last_backup_date}</TableCell>
                        <TableCell>{item.last_backup_time}</TableCell>
                        <TableCell>{item.last_deleted_date}</TableCell>
                        <TableCell>
                          {item.flag === "success" ? (
                            <img
                              src="/green-dot-icon.png"
                              alt="Success Icon"
                              style={{ width: "25px", height: "25px" }}
                            />
                          ) : item.flag === "warning" ? (
                            <img
                              src="/yellow-dot-icon.png"
                              alt="Warning Icon"
                              style={{ width: "25px", height: "25px" }}
                            />
                          ) : item.flag === "danger" ? (
                            <img
                              src="/red-dot-icon.png"
                              alt="Danger Icon"
                              style={{ width: "25px", height: "25px" }}
                            />
                          ) : (
                            <span>No Icon</span>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[10, 25, 50]}
              component="div"
              count={filteredData.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </div>
        </div>
      ) : (
        <div>
          <h1>Home Page</h1>
          <p>Loading...</p>
        </div>
      )}
    </>
  );
};

export default HomePage;
