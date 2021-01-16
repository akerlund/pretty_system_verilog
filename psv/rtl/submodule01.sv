module submodule01 (
  // Clock and reset
  input  wire  clk,
  input  wire                rst_n
);

submodule02 submodule02_i0 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);

endmodule