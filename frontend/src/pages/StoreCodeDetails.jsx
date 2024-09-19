import React, { useState, useEffect } from "react";
import { get } from "../api/api";
import { useParams } from "react-router-dom";
import {
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TablePagination,
  TableSortLabel,
  Paper,
  TextField,
  Button,
} from "@mui/material";
import exportToExcel from "../utils/convertToExcel";
import "./StoreCodeDetails.css";

const StoreCodeDetails = () => {
  const { storeCode } = useParams();
  const [data, setData] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("file_name");
  const [search, setSearch] = useState("");

  useEffect(() => {
    get("/store-code", {
      params: {
        store_code: storeCode,
      },
    })
      .then((res) => {
        setData(res.data);
        console.log(res);
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

  const stableSort = (array, comparator) => {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
  };

  const getComparator = (order, orderBy) => {
    return order === "desc"
      ? (a, b) => b[orderBy].localeCompare(a[orderBy])
      : (a, b) => a[orderBy].localeCompare(b[orderBy]);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearchChange = (event) => {
    const searchTerm = event.target.value;
    setSearch(searchTerm);
  };

  const filteredData = data
    ? data.filter((item) => {
        const isSizeString =
          typeof item.size === "string" || item.size instanceof String;

        return (
          item.file_name.toLowerCase().includes(search.toLowerCase()) ||
          item.store_code.toLowerCase().includes(search.toLowerCase()) ||
          (isSizeString &&
            item.size.toLowerCase().includes(search.toLowerCase())) ||
          item.date.toLowerCase().includes(search.toLowerCase()) ||
          item.time.toLowerCase().includes(search.toLowerCase())
        );
      })
    : [];

  const exportData = () => {
    const dataToExport = filteredData.map((item) => ({
      file_name: item.file_name,
      store_code: item.store_code,
      size: item.size,
      date: item.date,
      time: item.time,
      status: item.status,
    }));
    exportToExcel(dataToExport, `StoreCode-${storeCode}-backup-log`);
  };

  return (
    <>
      {data ? (
        <div>
          <h1>Store Code: {storeCode}</h1>
          <div className="search-and-export-container">
            <div className="search-container">
              <TextField
                label="Search"
                value={search}
                onChange={handleSearchChange}
                style={{ margin: "10px" }}
              />
              <Button
                style={{ margin: "10px" }}
                variant="contained"
                onClick={() => {
                  window.history.back();
                }}
              >
                Back
              </Button>
            </div>
            <Button
              style={{ margin: "10px" }}
              variant="contained"
              onClick={exportData}
            >
              Export to Excel
            </Button>
          </div>
          <div className="table-container">
            <TableContainer>
              <Table>
                <TableHead className="table-head">
                  <TableRow className="table-row">
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "file_name"}
                        direction={orderBy === "file_name" ? order : "asc"}
                        onClick={() => handleRequestSort("file_name")}
                      >
                        File Name
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "store_code"}
                        direction={orderBy === "store_code" ? order : "asc"}
                        onClick={() => handleRequestSort("store_code")}
                      >
                        Store Code
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "size"}
                        direction={orderBy === "size" ? order : "asc"}
                        onClick={() => handleRequestSort("size")}
                      >
                        Size
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "date"}
                        direction={orderBy === "date" ? order : "asc"}
                        onClick={() => handleRequestSort("date")}
                      >
                        Date
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "time"}
                        direction={orderBy === "time" ? order : "asc"}
                        onClick={() => handleRequestSort("time")}
                      >
                        Time
                      </TableSortLabel>
                    </TableCell>
                    <TableCell>
                      <TableSortLabel
                        active={orderBy === "status"}
                        direction={orderBy === "status" ? order : "asc"}
                        onClick={() => handleRequestSort("status")}
                      >
                        Status
                      </TableSortLabel>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody className="table-body">
                  {stableSort(filteredData, getComparator(order, orderBy))
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((item, index) => (
                      <TableRow key={index}>
                        <TableCell>{item.file_name}</TableCell>
                        <TableCell>{item.store_code}</TableCell>
                        <TableCell>{item.size}</TableCell>
                        <TableCell>{item.date}</TableCell>
                        <TableCell>{item.time}</TableCell>
                        <TableCell>{item.status}</TableCell>
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
        <h1>Loading...</h1>
      )}
    </>
  );
};

export default StoreCodeDetails;
