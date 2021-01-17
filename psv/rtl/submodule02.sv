module submodule02 (
  // Clock and reset
  input  wire  clk,
  input  wire                rst_n
);


submodule03 submodule03_i0 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);


submodule03 submodule03_i1 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);


submodule03 submodule03_i2 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);


submodule03 submodule03_i3 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);


endmodule