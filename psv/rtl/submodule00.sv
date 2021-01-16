module submodule00 (
  // Clock and reset
  input  wire  clk,
  input  wire                rst_n
);

submodule01 submodule01_i0 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);

submodule01 submodule01_i1 (
  .clk   ( clk ),
  .rst_n ( rst_n )
);

endmodule